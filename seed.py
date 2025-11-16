"""
Script de Inicialización de Datos
CiberSegurIA - Diagnóstico SGSI Express MVP

Carga preguntas iniciales basadas en:
- ISO/IEC 27001:2022 Anexo A
- Ley Marco de Ciberseguridad 21.663 (Chile)
- Ley 21.096 de Protección de Datos Personales

Ejecutar con: python seed.py
"""
from database import SessionLocal, engine
import models

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)


def seed_questions():
    """Poblar la base de datos con preguntas del cuestionario SGSI"""
    db = SessionLocal()

    # Verificar si ya existen preguntas
    existing_count = db.query(models.Question).count()
    if existing_count > 0:
        print(f"⚠️  Ya existen {existing_count} preguntas en la base de datos.")
        response = input("¿Deseas eliminar todas y recargar? (s/N): ")
        if response.lower() != 's':
            print("Operación cancelada.")
            return
        # Eliminar todas las preguntas existentes
        db.query(models.Question).delete()
        db.commit()
        print("✓ Preguntas anteriores eliminadas.")

    # Lista de preguntas basadas en ISO 27001 y Ley 21.663
    questions = [
        # ================================================================
        # A.5 POLÍTICAS DE SEGURIDAD DE LA INFORMACIÓN
        # ================================================================
        {
            "dominio": "A.5 Políticas de Seguridad",
            "subdominio": "A.5.1 Dirección de la Gestión para la Seguridad de la Información",
            "pregunta": "¿La organización cuenta con una Política de Seguridad de la Información formalmente aprobada por la alta dirección?",
            "descripcion": "Debe existir un documento formal que establezca el compromiso de la alta dirección con la seguridad de la información.",
            "peso": 5,
            "orden": 1,
            "referencia_legal": "ISO 27001:2022 A.5.1 | Art. 4 Ley 21.663"
        },
        {
            "dominio": "A.5 Políticas de Seguridad",
            "subdominio": "A.5.1 Dirección de la Gestión para la Seguridad de la Información",
            "pregunta": "¿La Política de Seguridad se revisa y actualiza periódicamente (al menos anualmente)?",
            "descripcion": "Las políticas deben mantenerse actualizadas frente a cambios en el negocio, tecnología y amenazas.",
            "peso": 3,
            "orden": 2,
            "referencia_legal": "ISO 27001:2022 A.5.1"
        },

        # ================================================================
        # A.6 ORGANIZACIÓN DE LA SEGURIDAD DE LA INFORMACIÓN
        # ================================================================
        {
            "dominio": "A.6 Organización de la Seguridad",
            "subdominio": "A.6.1 Estructura Organizacional",
            "pregunta": "¿Existe un responsable designado para la seguridad de la información (CISO o equivalente)?",
            "descripcion": "Debe haber una persona con autoridad y recursos para coordinar la seguridad de la información.",
            "peso": 5,
            "orden": 3,
            "referencia_legal": "ISO 27001:2022 A.6.1 | Art. 5 Ley 21.663"
        },
        {
            "dominio": "A.6 Organización de la Seguridad",
            "subdominio": "A.6.2 Dispositivos Móviles y Teletrabajo",
            "pregunta": "¿Existen políticas y controles específicos para el uso de dispositivos móviles y teletrabajo?",
            "descripcion": "Incluye BYOD, acceso remoto, VPN, y seguridad de dispositivos fuera de las instalaciones.",
            "peso": 4,
            "orden": 4,
            "referencia_legal": "ISO 27001:2022 A.6.7"
        },

        # ================================================================
        # A.8 GESTIÓN DE ACTIVOS
        # ================================================================
        {
            "dominio": "A.8 Gestión de Activos",
            "subdominio": "A.8.1 Inventario de Activos",
            "pregunta": "¿La organización mantiene un inventario actualizado de todos los activos de información (hardware, software, datos)?",
            "descripcion": "El inventario debe incluir propietarios, clasificación y ubicación de los activos.",
            "peso": 5,
            "orden": 5,
            "referencia_legal": "ISO 27001:2022 A.5.9 | Art. 6 Ley 21.663"
        },
        {
            "dominio": "A.8 Gestión de Activos",
            "subdominio": "A.8.2 Clasificación de la Información",
            "pregunta": "¿Se clasifican los activos de información según su criticidad y sensibilidad (ej: Público, Interno, Confidencial, Restringido)?",
            "descripcion": "La clasificación permite aplicar controles de seguridad proporcionales al valor de la información.",
            "peso": 4,
            "orden": 6,
            "referencia_legal": "ISO 27001:2022 A.5.12"
        },
        {
            "dominio": "A.8 Gestión de Activos",
            "subdominio": "A.8.3 Manejo de Medios",
            "pregunta": "¿Existe un procedimiento seguro para la eliminación o reutilización de medios de almacenamiento?",
            "descripcion": "Incluye borrado seguro de discos, destrucción de medios físicos y sanitización de equipos.",
            "peso": 4,
            "orden": 7,
            "referencia_legal": "ISO 27001:2022 A.7.14"
        },

        # ================================================================
        # A.9 CONTROL DE ACCESO
        # ================================================================
        {
            "dominio": "A.9 Control de Acceso",
            "subdominio": "A.9.1 Política de Control de Acceso",
            "pregunta": "¿Existe una política formal de control de acceso basada en el principio de menor privilegio?",
            "descripcion": "Los usuarios deben tener únicamente los accesos necesarios para realizar sus funciones.",
            "peso": 5,
            "orden": 8,
            "referencia_legal": "ISO 27001:2022 A.5.15 | Art. 7 Ley 21.663"
        },
        {
            "dominio": "A.9 Control de Acceso",
            "subdominio": "A.9.2 Gestión de Acceso de Usuarios",
            "pregunta": "¿Se realiza un proceso formal de alta, modificación y baja de usuarios en los sistemas?",
            "descripcion": "Debe existir un proceso documentado para gestionar el ciclo de vida de las cuentas de usuario.",
            "peso": 5,
            "orden": 9,
            "referencia_legal": "ISO 27001:2022 A.5.16"
        },
        {
            "dominio": "A.9 Control de Acceso",
            "subdominio": "A.9.3 Autenticación de Usuarios",
            "pregunta": "¿Se implementa autenticación multifactor (MFA/2FA) para el acceso a sistemas críticos?",
            "descripcion": "MFA proporciona una capa adicional de seguridad más allá de las contraseñas.",
            "peso": 4,
            "orden": 10,
            "referencia_legal": "ISO 27001:2022 A.5.17"
        },
        {
            "dominio": "A.9 Control de Acceso",
            "subdominio": "A.9.4 Revisión de Derechos de Acceso",
            "pregunta": "¿Se revisan periódicamente los derechos de acceso de los usuarios para verificar su vigencia?",
            "descripcion": "Las revisiones deben realizarse al menos trimestralmente para sistemas críticos.",
            "peso": 3,
            "orden": 11,
            "referencia_legal": "ISO 27001:2022 A.5.18"
        },

        # ================================================================
        # A.10 CRIPTOGRAFÍA
        # ================================================================
        {
            "dominio": "A.10 Criptografía",
            "subdominio": "A.10.1 Controles Criptográficos",
            "pregunta": "¿Se utiliza cifrado para proteger información sensible en tránsito (ej: TLS/SSL, VPN)?",
            "descripcion": "Las comunicaciones que transportan información sensible deben estar cifradas.",
            "peso": 5,
            "orden": 12,
            "referencia_legal": "ISO 27001:2022 A.8.24 | Ley 21.096 Art. 9"
        },
        {
            "dominio": "A.10 Criptografía",
            "subdominio": "A.10.1 Controles Criptográficos",
            "pregunta": "¿Se utiliza cifrado para proteger información sensible en reposo (bases de datos, backups, discos)?",
            "descripcion": "Los datos personales y críticos almacenados deben estar cifrados.",
            "peso": 4,
            "orden": 13,
            "referencia_legal": "ISO 27001:2022 A.8.24 | Ley 21.096 Art. 9"
        },

        # ================================================================
        # A.12 SEGURIDAD EN LAS OPERACIONES
        # ================================================================
        {
            "dominio": "A.12 Seguridad en las Operaciones",
            "subdominio": "A.12.1 Procedimientos Operacionales",
            "pregunta": "¿Existen procedimientos documentados para la operación y administración de los sistemas de información?",
            "descripcion": "Incluye procedimientos de backup, monitoreo, gestión de logs, etc.",
            "peso": 3,
            "orden": 14,
            "referencia_legal": "ISO 27001:2022 A.5.37"
        },
        {
            "dominio": "A.12 Seguridad en las Operaciones",
            "subdominio": "A.12.2 Protección contra Malware",
            "pregunta": "¿Se utilizan soluciones antimalware actualizadas en todos los endpoints y servidores?",
            "descripcion": "Debe existir protección activa contra virus, ransomware y otro software malicioso.",
            "peso": 5,
            "orden": 15,
            "referencia_legal": "ISO 27001:2022 A.8.7"
        },
        {
            "dominio": "A.12 Seguridad en las Operaciones",
            "subdominio": "A.12.3 Respaldos (Backups)",
            "pregunta": "¿Se realizan backups periódicos de la información crítica y se prueban las restauraciones?",
            "descripcion": "Los backups deben realizarse regularmente y las restauraciones deben probarse al menos semestralmente.",
            "peso": 5,
            "orden": 16,
            "referencia_legal": "ISO 27001:2022 A.8.13"
        },
        {
            "dominio": "A.12 Seguridad en las Operaciones",
            "subdominio": "A.12.4 Registro y Monitoreo",
            "pregunta": "¿Se registran y monitorean los eventos de seguridad en sistemas críticos (logs de acceso, cambios, errores)?",
            "descripcion": "Los logs deben conservarse por al menos 90 días y revisarse periódicamente.",
            "peso": 4,
            "orden": 17,
            "referencia_legal": "ISO 27001:2022 A.8.15 | Art. 13 Ley 21.663"
        },
        {
            "dominio": "A.12 Seguridad en las Operaciones",
            "subdominio": "A.12.6 Gestión de Vulnerabilidades Técnicas",
            "pregunta": "¿Se realiza gestión de parches de seguridad en sistemas operativos y aplicaciones de forma oportuna?",
            "descripcion": "Los parches críticos deben aplicarse dentro de los 30 días de su publicación.",
            "peso": 5,
            "orden": 18,
            "referencia_legal": "ISO 27001:2022 A.8.8"
        },

        # ================================================================
        # A.13 SEGURIDAD EN LAS COMUNICACIONES
        # ================================================================
        {
            "dominio": "A.13 Seguridad en las Comunicaciones",
            "subdominio": "A.13.1 Seguridad en Redes",
            "pregunta": "¿Se utilizan firewalls y segmentación de red para proteger los recursos de información?",
            "descripcion": "Las redes deben estar segmentadas (DMZ, servidores, usuarios) con controles de firewall.",
            "peso": 5,
            "orden": 19,
            "referencia_legal": "ISO 27001:2022 A.8.20"
        },

        # ================================================================
        # A.14 ADQUISICIÓN, DESARROLLO Y MANTENIMIENTO DE SISTEMAS
        # ================================================================
        {
            "dominio": "A.14 Desarrollo y Mantenimiento de Sistemas",
            "subdominio": "A.14.2 Seguridad en el Desarrollo",
            "pregunta": "¿Se incluyen requisitos de seguridad en el ciclo de desarrollo de software (Secure SDLC)?",
            "descripcion": "La seguridad debe integrarse desde el diseño, no agregarse al final.",
            "peso": 3,
            "orden": 20,
            "referencia_legal": "ISO 27001:2022 A.8.25"
        },

        # ================================================================
        # A.16 GESTIÓN DE INCIDENTES DE SEGURIDAD
        # ================================================================
        {
            "dominio": "A.16 Gestión de Incidentes",
            "subdominio": "A.16.1 Respuesta a Incidentes",
            "pregunta": "¿Existe un procedimiento documentado para la detección, reporte y respuesta a incidentes de seguridad?",
            "descripcion": "Debe incluir roles, responsabilidades, canales de escalamiento y procedimientos de contención.",
            "peso": 5,
            "orden": 21,
            "referencia_legal": "ISO 27001:2022 A.5.24 | Art. 14 Ley 21.663"
        },
        {
            "dominio": "A.16 Gestión de Incidentes",
            "subdominio": "A.16.1 Respuesta a Incidentes",
            "pregunta": "¿Se han definido y comunicado los plazos para notificar incidentes de ciberseguridad a las autoridades competentes?",
            "descripcion": "La Ley 21.663 establece plazos específicos para notificación de incidentes a la autoridad.",
            "peso": 5,
            "orden": 22,
            "referencia_legal": "Art. 15 Ley 21.663 (Notificación de Incidentes)"
        },

        # ================================================================
        # A.17 CONTINUIDAD DEL NEGOCIO
        # ================================================================
        {
            "dominio": "A.17 Continuidad del Negocio",
            "subdominio": "A.17.1 Gestión de Continuidad",
            "pregunta": "¿Existe un Plan de Continuidad del Negocio (BCP) y/o Plan de Recuperación de Desastres (DRP)?",
            "descripcion": "Debe documentar cómo mantener o recuperar las operaciones críticas ante incidentes mayores.",
            "peso": 4,
            "orden": 23,
            "referencia_legal": "ISO 27001:2022 A.5.29"
        },
        {
            "dominio": "A.17 Continuidad del Negocio",
            "subdominio": "A.17.1 Gestión de Continuidad",
            "pregunta": "¿Se prueban y actualizan periódicamente los planes de continuidad del negocio?",
            "descripcion": "Los planes deben probarse al menos anualmente mediante ejercicios o simulacros.",
            "peso": 3,
            "orden": 24,
            "referencia_legal": "ISO 27001:2022 A.5.30"
        },

        # ================================================================
        # A.18 CUMPLIMIENTO
        # ================================================================
        {
            "dominio": "A.18 Cumplimiento Legal y Contractual",
            "subdominio": "A.18.1 Cumplimiento de Requisitos Legales",
            "pregunta": "¿La organización identifica y cumple con todos los requisitos legales aplicables en materia de protección de datos y ciberseguridad?",
            "descripcion": "Incluye Ley 21.663, Ley 21.096, y otras regulaciones sectoriales aplicables.",
            "peso": 5,
            "orden": 25,
            "referencia_legal": "ISO 27001:2022 A.5.31 | Ley 21.096 | Ley 21.663"
        },
        {
            "dominio": "A.18 Cumplimiento Legal y Contractual",
            "subdominio": "A.18.1 Cumplimiento de Requisitos Legales",
            "pregunta": "¿Se han implementado los derechos de los titulares de datos personales (ARCO: Acceso, Rectificación, Cancelación, Oposición)?",
            "descripcion": "Debe existir un proceso formal para que los ciudadanos ejerzan sus derechos sobre sus datos.",
            "peso": 4,
            "orden": 26,
            "referencia_legal": "Ley 21.096 Art. 12-16"
        },

        # ================================================================
        # CONCIENCIACIÓN Y CAPACITACIÓN
        # ================================================================
        {
            "dominio": "A.7 Seguridad en Recursos Humanos",
            "subdominio": "A.7.2 Capacitación y Concienciación",
            "pregunta": "¿Se imparte capacitación periódica en seguridad de la información y ciberseguridad a todos los empleados?",
            "descripcion": "La capacitación debe ser al menos anual y cubrir temas como phishing, manejo de contraseñas, etc.",
            "peso": 4,
            "orden": 27,
            "referencia_legal": "ISO 27001:2022 A.6.3 | Art. 8 Ley 21.663"
        },

        # ================================================================
        # GESTIÓN DE RIESGOS
        # ================================================================
        {
            "dominio": "A.5 Políticas de Seguridad",
            "subdominio": "A.5.7 Gestión de Riesgos",
            "pregunta": "¿Se realiza una evaluación de riesgos de seguridad de la información de forma periódica (al menos anualmente)?",
            "descripcion": "La evaluación debe identificar amenazas, vulnerabilidades, impactos y definir tratamientos.",
            "peso": 5,
            "orden": 28,
            "referencia_legal": "ISO 27001:2022 Cláusula 6.1 | Art. 10 Ley 21.663"
        },

        # ================================================================
        # TERCEROS Y PROVEEDORES
        # ================================================================
        {
            "dominio": "A.15 Relaciones con Proveedores",
            "subdominio": "A.15.1 Seguridad en las Relaciones con Proveedores",
            "pregunta": "¿Se incluyen cláusulas de seguridad de la información en los contratos con terceros y proveedores?",
            "descripcion": "Los contratos deben especificar requisitos de seguridad, SLAs, auditorías y responsabilidades.",
            "peso": 4,
            "orden": 29,
            "referencia_legal": "ISO 27001:2022 A.5.19"
        },
        {
            "dominio": "A.15 Relaciones con Proveedores",
            "subdominio": "A.15.2 Gestión de Servicios de Terceros",
            "pregunta": "¿Se monitorea y revisa el desempeño de seguridad de los proveedores críticos?",
            "descripcion": "Debe existir supervisión periódica del cumplimiento de seguridad por parte de proveedores.",
            "peso": 3,
            "orden": 30,
            "referencia_legal": "ISO 27001:2022 A.5.20"
        }
    ]

    # Insertar preguntas
    print("📝 Insertando preguntas en la base de datos...")
    for q_data in questions:
        question = models.Question(**q_data)
        db.add(question)

    db.commit()
    print(f"✅ {len(questions)} preguntas insertadas correctamente.")
    print("\n📊 Resumen por dominio:")

    # Contar por dominio
    dominios = db.query(models.Question.dominio, models.Question).all()
    dominio_count = {}
    for dominio, _ in dominios:
        dominio_count[dominio] = dominio_count.get(dominio, 0) + 1

    for dominio, count in sorted(dominio_count.items()):
        print(f"   {dominio}: {count} preguntas")

    db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("CiberSegurIA - Inicialización de Base de Datos")
    print("=" * 70)
    print()
    seed_questions()
    print()
    print("=" * 70)
    print("✅ Proceso completado. La aplicación está lista para usar.")
    print("=" * 70)
    print()
    print("Próximos pasos:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Ejecutar servidor: uvicorn main:app --reload")
    print("3. Abrir navegador: http://localhost:8000")
    print()
