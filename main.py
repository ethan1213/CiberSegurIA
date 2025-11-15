"""
Aplicación Principal FastAPI
CiberSegurIA - Diagnóstico SGSI Express MVP
"""
from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

import models
import auth
from database import engine, get_db
from pdf_generator import generate_assessment_report

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="CiberSegurIA - Diagnóstico SGSI Express",
    description="Plataforma de diagnóstico de cumplimiento Ley 21.663",
    version="1.0.0"
)

# Middleware de sesiones (necesario para cookies)
app.add_middleware(SessionMiddleware, secret_key="ciberseguria-session-secret-changeme")

# Archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ============================================================================
# RUTAS PÚBLICAS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página de inicio"""
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    rut: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Procesar login"""
    # Autenticar usuario
    user = auth.authenticate_user(db, rut, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "RUT o contraseña incorrectos"}
        )

    # Crear sesión
    request.session["user_id"] = user.id

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(
    request: Request,
    nombre_empresa: str = Form(...),
    rut: str = Form(...),
    email_contacto: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    db: Session = Depends(get_db)
):
    """Procesar registro de nueva empresa"""
    # Validaciones
    errors = []

    if password != password_confirm:
        errors.append("Las contraseñas no coinciden")

    # Verificar si el RUT ya existe
    existing_user = db.query(models.User).filter(models.User.rut == rut).first()
    if existing_user:
        errors.append("El RUT ya está registrado")

    # Verificar si el email ya existe
    existing_email = db.query(models.User).filter(models.User.email_contacto == email_contacto).first()
    if existing_email:
        errors.append("El email ya está registrado")

    if errors:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "errors": errors}
        )

    # Crear nuevo usuario
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(
        nombre_empresa=nombre_empresa,
        rut=rut,
        email_contacto=email_contacto,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto-login
    request.session["user_id"] = new_user.id

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/logout")
async def logout(request: Request):
    """Cerrar sesión"""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# ============================================================================
# RUTAS PROTEGIDAS
# ============================================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Dashboard principal - Mostrar diagnósticos anteriores"""
    # Obtener assessments del usuario
    assessments = db.query(models.Assessment).filter(
        models.Assessment.user_id == current_user.id
    ).order_by(models.Assessment.fecha.desc()).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "assessments": assessments
        }
    )


@app.get("/assessment/new")
async def new_assessment(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Crear un nuevo assessment y redirigir al cuestionario"""
    # Crear nuevo assessment
    new_assessment = models.Assessment(
        user_id=current_user.id,
        estado="En Progreso"
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return RedirectResponse(
        url=f"/assessment/{new_assessment.id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/assessment/{assessment_id}", response_class=HTMLResponse)
async def assessment_questions(
    request: Request,
    assessment_id: int,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Mostrar cuestionario de assessment"""
    # Verificar que el assessment pertenece al usuario
    assessment = db.query(models.Assessment).filter(
        models.Assessment.id == assessment_id,
        models.Assessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")

    # Si ya está completado, redirigir al reporte
    if assessment.estado == "Completado":
        return RedirectResponse(
            url=f"/assessment/report/{assessment_id}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Obtener todas las preguntas ordenadas
    questions = db.query(models.Question).order_by(
        models.Question.dominio,
        models.Question.orden
    ).all()

    # Agrupar preguntas por dominio
    questions_by_domain = {}
    for q in questions:
        if q.dominio not in questions_by_domain:
            questions_by_domain[q.dominio] = []
        questions_by_domain[q.dominio].append(q)

    # Obtener respuestas existentes (si las hay)
    existing_answers = {}
    for answer in assessment.answers:
        existing_answers[answer.question_id] = {
            'respuesta': answer.respuesta.value,
            'evidencia': answer.evidencia_adjunta or ''
        }

    return templates.TemplateResponse(
        "assessment.html",
        {
            "request": request,
            "user": current_user,
            "assessment": assessment,
            "questions_by_domain": questions_by_domain,
            "existing_answers": existing_answers,
            "RespuestaEnum": models.RespuestaEnum
        }
    )


@app.post("/assessment/{assessment_id}/submit")
async def submit_assessment(
    request: Request,
    assessment_id: int,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Procesar y guardar respuestas del cuestionario"""
    # Verificar que el assessment pertenece al usuario
    assessment = db.query(models.Assessment).filter(
        models.Assessment.id == assessment_id,
        models.Assessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")

    # Obtener datos del formulario
    form_data = await request.form()

    # Obtener todas las preguntas
    questions = db.query(models.Question).all()

    # Borrar respuestas anteriores (si existen)
    db.query(models.Answer).filter(models.Answer.assessment_id == assessment_id).delete()

    # Procesar respuestas
    total_weight = 0
    total_score = 0

    for question in questions:
        respuesta_key = f"question_{question.id}"
        evidencia_key = f"evidencia_{question.id}"

        respuesta_value = form_data.get(respuesta_key)
        evidencia_value = form_data.get(evidencia_key, "")

        if not respuesta_value:
            continue

        # Convertir respuesta a enum
        respuesta_enum = models.RespuestaEnum(respuesta_value)

        # Crear answer
        answer = models.Answer(
            assessment_id=assessment_id,
            question_id=question.id,
            respuesta=respuesta_enum,
            evidencia_adjunta=evidencia_value if evidencia_value else None
        )
        db.add(answer)

        # Calcular puntaje
        if respuesta_enum != models.RespuestaEnum.NA:
            total_weight += question.peso

            if respuesta_enum == models.RespuestaEnum.SI:
                total_score += question.peso * 100
            elif respuesta_enum == models.RespuestaEnum.PARCIAL:
                total_score += question.peso * 50

    # Calcular puntaje final
    if total_weight > 0:
        puntaje_final = total_score / total_weight
    else:
        puntaje_final = 0

    # Actualizar assessment
    assessment.puntaje_final = round(puntaje_final, 1)
    assessment.estado = "Completado"

    db.commit()

    # Redirigir a página de éxito/reporte
    return RedirectResponse(
        url=f"/assessment/report/{assessment_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/assessment/report/{assessment_id}", response_class=HTMLResponse)
async def view_report(
    request: Request,
    assessment_id: int,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Ver página de reporte con opción de descargar PDF"""
    # Verificar que el assessment pertenece al usuario
    assessment = db.query(models.Assessment).filter(
        models.Assessment.id == assessment_id,
        models.Assessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")

    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "user": current_user,
            "assessment": assessment
        }
    )


@app.get("/assessment/report/{assessment_id}/download")
async def download_report(
    assessment_id: int,
    current_user: models.User = Depends(auth.get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Generar y descargar PDF del reporte"""
    # Verificar que el assessment pertenece al usuario
    assessment = db.query(models.Assessment).filter(
        models.Assessment.id == assessment_id,
        models.Assessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")

    # Generar PDF
    pdf_path = generate_assessment_report(assessment_id, db)

    # Retornar archivo
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"Reporte_SGSI_{current_user.nombre_empresa}_{assessment_id}.pdf"
    )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "CiberSegurIA SGSI Express MVP"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
