# CiberSegurIA - Diagnóstico SGSI Express MVP

🔒 **Plataforma SaaS B2B para Diagnóstico de Cumplimiento de la Ley Marco de Ciberseguridad 21.663 (Chile)**

## 📋 Descripción

**Diagnóstico SGSI Express** es un MVP (Producto Mínimo Viable) diseñado como lead magnet para empresas chilenas que necesitan cumplir con la **Ley 21.663 de Ciberseguridad** y la **Ley 21.096 de Protección de Datos Personales**.

La plataforma permite a PYMEs y empresas Mid-Market realizar un autodiagnóstico de cumplimiento basado en:
- ✅ ISO/IEC 27001:2022
- ✅ Ley Marco de Ciberseguridad 21.663
- ✅ Ley 21.096 de Protección de Datos

### 🎯 Objetivo del Negocio

Este MVP funciona como **tripwire/gancho** para:
1. Las empresas completan un cuestionario de diagnóstico (30 preguntas)
2. Obtienen un **reporte PDF profesional** con:
   - Puntaje de cumplimiento (0-100%)
   - Análisis de brechas críticas (Gap Analysis)
   - Recomendaciones personalizadas
3. El reporte sirve como **excusa perfecta** para vender servicios de consultoría y remediación

---

## 🚀 Características

### ✅ Para Usuarios (Empresas)
- Registro simple con RUT y datos de empresa
- Cuestionario intuitivo con 30 preguntas clave
- Respuestas: Sí / No / Parcial / N/A
- Campo opcional para evidencias/comentarios
- Cálculo automático de puntaje de cumplimiento
- **Reporte PDF profesional** descargable
- Dashboard para gestionar múltiples diagnósticos

### ✅ Para CiberSegurIA (Nosotros)
- Base de datos de leads calificados
- Información valiosa sobre el estado de seguridad de prospectos
- Call-to-Action integrado en reportes
- Escalable para agregar funcionalidades premium

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|-----------|
| **Backend** | FastAPI (Python 3.9+) |
| **Base de Datos** | SQLite |
| **ORM** | SQLAlchemy |
| **Templates** | Jinja2 |
| **Autenticación** | JWT + Sesiones (Passlib + python-jose) |
| **Generación PDF** | ReportLab |
| **Servidor** | Uvicorn |

---

## 📁 Estructura del Proyecto

```
CiberSegurIA/
├── main.py                 # Aplicación FastAPI principal
├── models.py               # Modelos de base de datos (SQLAlchemy)
├── database.py             # Configuración de SQLAlchemy
├── auth.py                 # Sistema de autenticación
├── pdf_generator.py        # Generador de reportes PDF
├── seed.py                 # Script para cargar preguntas iniciales
├── requirements.txt        # Dependencias de Python
├── README.md               # Este archivo
│
├── templates/              # Templates HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── assessment.html
│   └── success.html
│
├── static/                 # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── logo.png (agregar tu logo aquí)
│
├── reports/                # PDFs generados (creado automáticamente)
└── ciberseguria.db         # Base de datos SQLite (creado al ejecutar)
```

---

## 🔧 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### 2. Clonar o Descargar el Proyecto
```bash
cd CiberSegurIA
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar Base de Datos con Preguntas
```bash
python seed.py
```

Esto creará:
- ✅ Base de datos SQLite (`ciberseguria.db`)
- ✅ 30 preguntas basadas en ISO 27001 y Ley 21.663

### 5. Ejecutar el Servidor
```bash
uvicorn main:app --reload
```

### 6. Abrir en el Navegador
```
http://localhost:8000
```

---

## 📖 Uso de la Plataforma

### Para Empresas (Usuarios Finales)

1. **Registro**
   - Ir a http://localhost:8000/register
   - Completar: Nombre Empresa, RUT, Email, Contraseña
   - Click en "Crear Cuenta"

2. **Completar Diagnóstico**
   - Click en "+ Nuevo Diagnóstico"
   - Responder las 30 preguntas organizadas por dominios
   - Opcionalmente agregar evidencias/comentarios
   - Click en "Generar Reporte de Diagnóstico"

3. **Descargar Reporte**
   - Ver el puntaje de cumplimiento
   - Descargar el PDF profesional
   - El reporte incluye:
     - Resumen ejecutivo con gráfico
     - Gap analysis (brechas críticas)
     - Recomendaciones
     - Detalle completo de respuestas

---

## 📊 Modelos de Base de Datos

### `User` (Empresas)
- `id`: ID único
- `nombre_empresa`: Razón social
- `rut`: RUT de la empresa (único)
- `email_contacto`: Email (único)
- `hashed_password`: Contraseña hasheada
- `created_at`: Fecha de registro

### `Assessment` (Diagnósticos)
- `id`: ID único
- `user_id`: FK a User
- `fecha`: Fecha/hora del diagnóstico
- `puntaje_final`: Puntaje 0-100%
- `estado`: "En Progreso" o "Completado"

### `Question` (Preguntas)
- `id`: ID único
- `dominio`: Ej. "A.5 Políticas de Seguridad"
- `subdominio`: Subdivisión
- `pregunta`: Texto de la pregunta
- `descripcion`: Contexto adicional
- `peso`: Criticidad (1-5)
- `orden`: Orden de presentación
- `referencia_legal`: Ej. "Art. 4 Ley 21.663"

### `Answer` (Respuestas)
- `id`: ID único
- `assessment_id`: FK a Assessment
- `question_id`: FK a Question
- `respuesta`: Enum (Sí, No, Parcial, N/A)
- `evidencia_adjunta`: Texto opcional

---

## 🎨 Personalización

### Cambiar Logo
1. Reemplazar `static/img/logo.png` con tu logo
2. Dimensiones recomendadas: 400x200 px

### Modificar Colores
Los colores principales están en `templates/base.html`:
- **Primario**: `#667eea` (azul/morado)
- **Secundario**: `#764ba2` (morado)
- **Éxito**: `#10b981` (verde)
- **Error**: `#ef4444` (rojo)

### Agregar/Modificar Preguntas
Editar `seed.py` y volver a ejecutar:
```bash
python seed.py
```

### Cambiar Secret Keys (IMPORTANTE EN PRODUCCIÓN)
En `auth.py` y `main.py`, cambiar:
```python
SECRET_KEY = "tu-secret-key-super-segura-aqui"
```

---

## 🔐 Seguridad

⚠️ **IMPORTANTE PARA PRODUCCIÓN:**

1. **Cambiar Secret Keys**
   - `auth.py`: SECRET_KEY
   - `main.py`: SessionMiddleware secret_key

2. **Usar PostgreSQL o MySQL**
   - SQLite es solo para desarrollo/MVP
   - Cambiar `database.py` para producción

3. **Habilitar HTTPS**
   - Usar certificados SSL/TLS

4. **Variables de Entorno**
   - No hardcodear secretos en el código
   - Usar `.env` con python-dotenv

5. **Rate Limiting**
   - Implementar slowapi o similar

6. **Validación de Datos**
   - Agregar Pydantic schemas más estrictos

---

## 📈 Roadmap de Funcionalidades Futuras

### Fase 2 (Post-MVP)
- [ ] Panel de administración
- [ ] Reportes comparativos (benchmarking)
- [ ] Exportación a Excel
- [ ] Integración con CRM (HubSpot, Salesforce)
- [ ] Notificaciones por email
- [ ] Planes de suscripción (Freemium)

### Fase 3
- [ ] Módulo de gestión de brechas (remediation tracker)
- [ ] Marketplace de consultores
- [ ] Auditorías asistidas por IA
- [ ] Integración con CSIRT Chile

---

## 🤝 Contribuciones

Este es un proyecto interno de CiberSegurIA. Para contribuir:
1. Contactar al CTO
2. Crear un branch desde `develop`
3. Pull Request con revisión de código

---

## 📞 Soporte

Para consultas técnicas o de negocio:
- **Email**: contacto@ciberseguria.cl
- **Equipo Técnico**: Ingenieros de Ciberseguridad + Infraestructura

---

## 📄 Licencia

© 2025 CiberSegurIA. Todos los derechos reservados.
Uso interno y comercial exclusivo.

---

## 🎉 ¡Listo para Lanzar!

El MVP está **completo y funcional**. Puedes:
1. ✅ Demostrar a inversores
2. ✅ Hacer pilotos con clientes beta
3. ✅ Integrarlo a tu embudo de ventas
4. ✅ Recolectar feedback para iterar

**¡Éxito con el lanzamiento! 🚀**