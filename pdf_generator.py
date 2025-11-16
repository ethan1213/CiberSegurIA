"""
Generador de Reportes PDF Profesionales
CiberSegurIA - Diagnóstico SGSI Express MVP
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from sqlalchemy.orm import Session
import models
import os


class PDFReportGenerator:
    """Generador de reportes de cumplimiento en PDF"""

    def __init__(self, assessment_id: int, db: Session):
        self.assessment_id = assessment_id
        self.db = db
        self.assessment = None
        self.user = None
        self.answers = []
        self.questions = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configurar estilos personalizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Texto normal justificado
        self.styles.add(ParagraphStyle(
            name='Justified',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            leading=14
        ))

    def _load_data(self):
        """Cargar datos del assessment desde la BD"""
        self.assessment = self.db.query(models.Assessment).filter(
            models.Assessment.id == self.assessment_id
        ).first()

        if not self.assessment:
            raise ValueError(f"Assessment {self.assessment_id} no encontrado")

        self.user = self.assessment.user
        self.answers = self.assessment.answers

    def _calculate_statistics(self):
        """Calcular estadísticas del assessment"""
        total_questions = len(self.answers)
        if total_questions == 0:
            return {
                'total': 0,
                'si': 0,
                'no': 0,
                'parcial': 0,
                'na': 0,
                'puntaje': 0
            }

        si_count = sum(1 for a in self.answers if a.respuesta == models.RespuestaEnum.SI)
        no_count = sum(1 for a in self.answers if a.respuesta == models.RespuestaEnum.NO)
        parcial_count = sum(1 for a in self.answers if a.respuesta == models.RespuestaEnum.PARCIAL)
        na_count = sum(1 for a in self.answers if a.respuesta == models.RespuestaEnum.NA)

        # Calcular puntaje (Si = 100%, Parcial = 50%, No = 0%, N/A no cuenta)
        total_evaluable = total_questions - na_count
        if total_evaluable > 0:
            puntaje = ((si_count * 100) + (parcial_count * 50)) / total_evaluable
        else:
            puntaje = 0

        return {
            'total': total_questions,
            'si': si_count,
            'no': no_count,
            'parcial': parcial_count,
            'na': na_count,
            'puntaje': round(puntaje, 1)
        }

    def _create_cover_page(self, story):
        """Crear portada del reporte"""
        # Logo (placeholder - si existe)
        logo_path = "static/img/logo.png"
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2*inch, height=1*inch)
            story.append(logo)
            story.append(Spacer(1, 0.5*inch))

        # Título principal
        title = Paragraph("REPORTE DE CUMPLIMIENTO<br/>LEY MARCO DE CIBERSEGURIDAD 21.663", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))

        # Subtítulo
        subtitle = Paragraph("Diagnóstico de Sistema de Gestión de Seguridad de la Información", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 1*inch))

        # Información de la empresa
        empresa_data = [
            ['Empresa:', self.user.nombre_empresa],
            ['RUT:', self.user.rut],
            ['Contacto:', self.user.email_contacto],
            ['Fecha de Evaluación:', self.assessment.fecha.strftime('%d/%m/%Y')],
            ['ID de Reporte:', f'SGSI-{self.assessment.id:04d}']
        ]

        empresa_table = Table(empresa_data, colWidths=[2*inch, 4*inch])
        empresa_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e3a8a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        story.append(empresa_table)
        story.append(Spacer(1, 1*inch))

        # Disclaimer
        disclaimer = Paragraph(
            "<b>CONFIDENCIAL:</b> Este reporte contiene información sensible sobre el estado de seguridad "
            "de la información de su organización. Debe ser tratado con la máxima confidencialidad.",
            self.styles['Justified']
        )
        story.append(disclaimer)
        story.append(PageBreak())

    def _create_executive_summary(self, story, stats):
        """Crear resumen ejecutivo con gráfico"""
        story.append(Paragraph("RESUMEN EJECUTIVO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))

        # Descripción
        intro = Paragraph(
            f"El presente reporte presenta los resultados del diagnóstico de cumplimiento realizado a "
            f"<b>{self.user.nombre_empresa}</b> en conformidad con los requisitos establecidos en la "
            f"Ley Marco de Ciberseguridad N° 21.663 y las mejores prácticas de ISO/IEC 27001:2022.",
            self.styles['Justified']
        )
        story.append(intro)
        story.append(Spacer(1, 0.3*inch))

        # Gráfico de dona con puntaje
        drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 150
        pie.y = 50
        pie.width = 120
        pie.height = 120

        # Datos del gráfico: Cumplimiento vs No Cumplimiento
        cumplimiento = stats['puntaje']
        no_cumplimiento = 100 - cumplimiento

        pie.data = [cumplimiento, no_cumplimiento]
        pie.labels = [f'Cumplimiento\n{cumplimiento}%', f'Brechas\n{no_cumplimiento}%']
        pie.slices[0].fillColor = colors.HexColor('#10b981')  # Verde
        pie.slices[1].fillColor = colors.HexColor('#ef4444')  # Rojo
        pie.slices[0].fontColor = colors.white
        pie.slices[1].fontColor = colors.white
        pie.slices[0].fontSize = 12
        pie.slices[1].fontSize = 12

        drawing.add(pie)
        story.append(drawing)
        story.append(Spacer(1, 0.3*inch))

        # Tabla de resumen
        summary_data = [
            ['MÉTRICA', 'VALOR'],
            ['Puntaje de Cumplimiento General', f'{stats["puntaje"]}%'],
            ['Total de Controles Evaluados', str(stats['total'])],
            ['Controles Implementados (Sí)', str(stats['si'])],
            ['Controles Parcialmente Implementados', str(stats['parcial'])],
            ['Controles No Implementados', str(stats['no'])],
            ['No Aplica', str(stats['na'])]
        ]

        summary_table = Table(summary_data, colWidths=[3.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')])
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

        # Nivel de riesgo
        if stats['puntaje'] >= 80:
            nivel = "CUMPLIMIENTO ALTO"
            color = colors.HexColor('#10b981')
            descripcion = "Su organización presenta un nivel alto de cumplimiento con la normativa vigente."
        elif stats['puntaje'] >= 50:
            nivel = "CUMPLIMIENTO MEDIO - ACCIÓN REQUERIDA"
            color = colors.HexColor('#f59e0b')
            descripcion = "Su organización presenta brechas significativas que requieren atención inmediata."
        else:
            nivel = "EN RIESGO CRÍTICO"
            color = colors.HexColor('#ef4444')
            descripcion = "Su organización presenta brechas críticas que exponen a riesgos regulatorios y operacionales graves."

        nivel_style = ParagraphStyle(
            name='Nivel',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=color,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        story.append(Paragraph(f"NIVEL DE CUMPLIMIENTO: {nivel}", nivel_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(descripcion, self.styles['Justified']))
        story.append(PageBreak())

    def _create_gap_analysis(self, story, stats):
        """Crear análisis de brechas (Gap Analysis)"""
        story.append(Paragraph("ANÁLISIS DE BRECHAS CRÍTICAS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))

        intro = Paragraph(
            "A continuación se presentan las principales brechas identificadas en su Sistema de Gestión "
            "de Seguridad de la Información, priorizadas por criticidad:",
            self.styles['Justified']
        )
        story.append(intro)
        story.append(Spacer(1, 0.3*inch))

        # Filtrar respuestas No y Parcial
        brechas = [
            a for a in self.answers
            if a.respuesta in [models.RespuestaEnum.NO, models.RespuestaEnum.PARCIAL]
        ]

        # Ordenar por peso de la pregunta (más críticas primero)
        brechas_sorted = sorted(brechas, key=lambda x: x.question.peso, reverse=True)[:10]

        if not brechas_sorted:
            story.append(Paragraph("¡Felicitaciones! No se identificaron brechas críticas.", self.styles['Normal']))
        else:
            gap_data = [['#', 'CONTROL', 'DOMINIO', 'ESTADO', 'PRIORIDAD']]

            for idx, answer in enumerate(brechas_sorted, 1):
                estado = "No Implementado" if answer.respuesta == models.RespuestaEnum.NO else "Parcial"
                prioridad = "ALTA" if answer.question.peso >= 4 else "MEDIA" if answer.question.peso >= 2 else "BAJA"

                gap_data.append([
                    str(idx),
                    Paragraph(answer.question.pregunta[:100] + "...", self.styles['Normal']),
                    answer.question.dominio,
                    estado,
                    prioridad
                ])

            gap_table = Table(gap_data, colWidths=[0.3*inch, 3*inch, 1.2*inch, 0.8*inch, 0.7*inch])
            gap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (-1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef2f2')])
            ]))
            story.append(gap_table)

        story.append(PageBreak())

    def _create_recommendations(self, story, stats):
        """Crear sección de recomendaciones (¡El Upsell!)"""
        story.append(Paragraph("RECOMENDACIONES Y PRÓXIMOS PASOS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))

        # Personalizar recomendaciones según puntaje
        num_brechas = stats['no'] + stats['parcial']

        recomendaciones = []

        if stats['puntaje'] < 50:
            recomendaciones = [
                "<b>1. Implementación Urgente de Programa de Cumplimiento:</b> Su organización requiere un programa "
                "integral de cumplimiento normativo que aborde las <b>{} brechas críticas</b> identificadas. "
                "Nuestro equipo de consultores especializados puede implementar un programa completo en <b>90 días</b>.".format(num_brechas),

                "<b>2. Capacitación de Personal:</b> Es fundamental capacitar a su equipo en los requisitos de la "
                "Ley 21.663 y mejores prácticas de ISO 27001. Ofrecemos programas de formación in-company certificados.",

                "<b>3. Evaluación de Riesgos Formal:</b> Recomendamos realizar una evaluación de riesgos profesional "
                "para priorizar las inversiones en seguridad de la información.",

                "<b>4. Desarrollo de Políticas y Procedimientos:</b> Necesita documentación formal de políticas, "
                "procedimientos y controles alineados con la normativa vigente."
            ]
        elif stats['puntaje'] < 80:
            recomendaciones = [
                "<b>1. Remediación de Brechas Identificadas:</b> Hemos identificado <b>{} brechas</b> que requieren "
                "atención. Podemos ayudarle a remediar estas brechas en menos de <b>60 días</b>.".format(num_brechas),

                "<b>2. Optimización de Controles Parciales:</b> Varios controles están parcialmente implementados. "
                "Podemos ayudarle a completar su implementación y documentación.",

                "<b>3. Auditoría Interna:</b> Recomendamos realizar una auditoría interna formal para validar "
                "el cumplimiento antes de una inspección regulatoria."
            ]
        else:
            recomendaciones = [
                "<b>1. Certificación ISO 27001:</b> Su nivel de madurez permite aspirar a una certificación "
                "internacional. Podemos guiarle en el proceso de certificación.",

                "<b>2. Mejora Continua:</b> Implementar un programa de mejora continua para mantener y elevar "
                "su nivel de cumplimiento.",

                "<b>3. Monitoreo y Revisión:</b> Establecer ciclos periódicos de revisión y actualización del SGSI."
            ]

        for rec in recomendaciones:
            story.append(Paragraph(rec, self.styles['Justified']))
            story.append(Spacer(1, 0.15*inch))

        story.append(Spacer(1, 0.3*inch))

        # Call to Action
        cta = Paragraph(
            "<b>¿CÓMO PODEMOS AYUDARLE?</b><br/><br/>"
            "En <b>CiberSegurIA</b> somos expertos en implementación de Sistemas de Gestión de Seguridad de la Información "
            "y cumplimiento normativo. Nuestro equipo de consultores certificados ha ayudado a decenas de organizaciones "
            "chilenas a alcanzar el cumplimiento total con la Ley 21.663.<br/><br/>"
            "<b>Agende una reunión sin costo con nuestros expertos:</b><br/>"
            "📧 Email: contacto@ciberseguria.cl<br/>"
            "📞 Teléfono: +56 2 XXXX XXXX<br/>"
            "🌐 Web: www.ciberseguria.cl",
            self.styles['Justified']
        )
        story.append(cta)
        story.append(PageBreak())

    def _create_detailed_results(self, story):
        """Crear anexo con resultados detallados"""
        story.append(Paragraph("ANEXO: DETALLE COMPLETO DE EVALUACIÓN", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))

        # Agrupar por dominio
        dominios = {}
        for answer in self.answers:
            dominio = answer.question.dominio
            if dominio not in dominios:
                dominios[dominio] = []
            dominios[dominio].append(answer)

        for dominio, answers in dominios.items():
            story.append(Paragraph(dominio, self.styles['CustomSubtitle']))
            story.append(Spacer(1, 0.1*inch))

            for answer in answers:
                # Color según respuesta
                if answer.respuesta == models.RespuestaEnum.SI:
                    color_bg = colors.HexColor('#d1fae5')
                    estado_text = '✓ Sí'
                elif answer.respuesta == models.RespuestaEnum.NO:
                    color_bg = colors.HexColor('#fee2e2')
                    estado_text = '✗ No'
                elif answer.respuesta == models.RespuestaEnum.PARCIAL:
                    color_bg = colors.HexColor('#fef3c7')
                    estado_text = '◐ Parcial'
                else:
                    color_bg = colors.HexColor('#f1f5f9')
                    estado_text = '− N/A'

                data = [
                    [Paragraph(f"<b>{answer.question.pregunta}</b>", self.styles['Normal'])],
                    [Paragraph(f"<b>Estado:</b> {estado_text}", self.styles['Normal'])],
                ]

                if answer.evidencia_adjunta:
                    data.append([Paragraph(f"<b>Evidencia:</b> {answer.evidencia_adjunta}", self.styles['Normal'])])

                detail_table = Table(data, colWidths=[6*inch])
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), color_bg),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1'))
                ]))
                story.append(detail_table)
                story.append(Spacer(1, 0.1*inch))

            story.append(Spacer(1, 0.2*inch))

    def generate_pdf(self, output_path: str = None) -> str:
        """Generar el PDF completo"""
        if not output_path:
            output_path = f"reports/reporte_sgsi_{self.assessment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Asegurar que existe el directorio
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Cargar datos
        self._load_data()

        # Calcular estadísticas
        stats = self._calculate_statistics()

        # Crear documento PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Story (contenido del PDF)
        story = []

        # Agregar secciones
        self._create_cover_page(story)
        self._create_executive_summary(story, stats)
        self._create_gap_analysis(story, stats)
        self._create_recommendations(story, stats)
        self._create_detailed_results(story)

        # Construir PDF
        doc.build(story)

        return output_path


def generate_assessment_report(assessment_id: int, db: Session) -> str:
    """Función helper para generar reporte"""
    generator = PDFReportGenerator(assessment_id, db)
    return generator.generate_pdf()
