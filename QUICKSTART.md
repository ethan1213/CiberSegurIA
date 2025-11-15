# 🚀 Guía de Inicio Rápido

Esta guía te llevará de 0 a 100 en **menos de 5 minutos**.

---

## ⚡ Instalación Express (3 Pasos)

### 1️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Cargar Datos Iniciales
```bash
python seed.py
```

### 3️⃣ Ejecutar Servidor
```bash
uvicorn main:app --reload
```

✅ **¡Listo!** Abre tu navegador en: http://localhost:8000

---

## 🎯 Prueba Rápida (Demo)

### Crear una Cuenta de Prueba
1. Ve a: http://localhost:8000/register
2. Completa el formulario:
   - **Empresa**: Acme Corp SpA
   - **RUT**: 12345678-9
   - **Email**: demo@acme.cl
   - **Contraseña**: demo1234

### Completar un Diagnóstico
1. Click en "**+ Nuevo Diagnóstico**"
2. Responde las 30 preguntas (puedes usar respuestas aleatorias para la demo)
3. Click en "**Generar Reporte de Diagnóstico**"

### Descargar tu Reporte PDF
1. Verás tu puntaje de cumplimiento
2. Click en "**📥 Descargar Reporte PDF Completo**"
3. Revisa el reporte profesional con:
   - Resumen ejecutivo
   - Gap analysis
   - Recomendaciones
   - Detalle completo

---

## 🐛 Solución de Problemas

### Error: "No module named 'fastapi'"
```bash
# Asegúrate de estar en el directorio correcto
cd CiberSegurIA
# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# El puerto 8000 está ocupado, usa otro puerto:
uvicorn main:app --reload --port 8080
```

### Error al generar PDF
```bash
# Verifica que exista el directorio reports/
mkdir -p reports
```

### La base de datos está corrupta
```bash
# Elimina la BD y vuelve a inicializar:
rm ciberseguria.db
python seed.py
```

---

## 📱 Endpoints Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Redirect a login |
| `/login` | Iniciar sesión |
| `/register` | Crear cuenta |
| `/dashboard` | Panel principal |
| `/assessment/new` | Nuevo diagnóstico |
| `/assessment/{id}` | Cuestionario |
| `/assessment/report/{id}` | Ver reporte |
| `/assessment/report/{id}/download` | Descargar PDF |
| `/health` | Health check |

---

## 🔑 Credenciales de Prueba Rápida

Si quieres saltarte el registro, puedes:

```bash
# Ejecutar el servidor
uvicorn main:app --reload

# En otra terminal, crear un usuario de prueba con Python:
python -c "
from database import SessionLocal
from auth import get_password_hash
import models

db = SessionLocal()
user = models.User(
    nombre_empresa='Demo Corp',
    rut='11111111-1',
    email_contacto='demo@demo.cl',
    hashed_password=get_password_hash('demo123')
)
db.add(user)
db.commit()
print('Usuario creado: demo@demo.cl / demo123')
"
```

Luego login con:
- **RUT**: 11111111-1
- **Password**: demo123

---

## 🎨 Personalización Rápida

### Cambiar el nombre de la empresa
Edita `templates/base.html` línea ~31:
```html
<div class="logo">TuEmpresa</div>
```

### Cambiar colores
Edita `templates/base.html` líneas ~16-20:
```css
background: linear-gradient(135deg, #TU_COLOR_1, #TU_COLOR_2);
```

### Agregar más preguntas
Edita `seed.py` y agrega al array `questions`, luego:
```bash
python seed.py  # Responde "s" para recargar
```

---

## 📦 Despliegue Rápido

### Opción 1: Render.com (Gratis)
1. Crea cuenta en render.com
2. New Web Service → Connect GitHub
3. Build Command: `pip install -r requirements.txt && python seed.py`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Opción 2: Railway.app (Gratis)
1. Instala Railway CLI
2. `railway login`
3. `railway init`
4. `railway up`

### Opción 3: Heroku
```bash
# Crear Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Desplegar
heroku create
git push heroku main
heroku run python seed.py
```

---

## ✅ Checklist Pre-Lanzamiento

Antes de lanzar a producción:

- [ ] Cambiar SECRET_KEY en `auth.py`
- [ ] Cambiar SessionMiddleware secret en `main.py`
- [ ] Reemplazar `static/img/logo.png` con tu logo
- [ ] Cambiar email de contacto en templates
- [ ] Migrar de SQLite a PostgreSQL
- [ ] Habilitar HTTPS
- [ ] Configurar backup automático de BD
- [ ] Testear en múltiples navegadores
- [ ] Agregar Google Analytics

---

**¿Problemas?** Consulta el README.md completo o contacta al equipo técnico.

**¡Buena suerte con tu MVP! 🎉**
