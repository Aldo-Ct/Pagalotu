#!/usr/bin/env python3
"""Genera el informe S01 en PDF con evidencias verificables del microservicio."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "s01"
OUTPUT = ROOT / "output" / "pdf" / "S01_SinGrupo_CallaAldo.pdf"

NAVY = colors.HexColor("#13293D")
BLUE = colors.HexColor("#1B6CA8")
TEAL = colors.HexColor("#168C8C")
CYAN = colors.HexColor("#DDF4F4")
GOLD = colors.HexColor("#F4B942")
INK = colors.HexColor("#22313F")
MUTED = colors.HexColor("#607485")
PAPER = colors.HexColor("#F7F9FB")
LINE = colors.HexColor("#D8E1E8")
WHITE = colors.white


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="S01Title", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=25, leading=30, textColor=WHITE, alignment=TA_LEFT,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="S01Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11.5, leading=16, textColor=colors.HexColor("#D9EEF5"),
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=17, leading=21, textColor=NAVY, spaceBefore=0, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=15, textColor=TEAL, spaceBefore=8, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyS01", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.4, leading=13.4, textColor=INK, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8.3, leading=11.5, textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableHeader", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=8.3, leading=11.5, textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="CoverValue", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8.3, leading=11.5, textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["BodyText"], fontName="Helvetica-Oblique",
    fontSize=7.7, leading=10.3, textColor=MUTED, alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Label", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=7.4, leading=9, textColor=TEAL, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="CodeS01", parent=styles["Code"], fontName="Courier",
    fontSize=7.6, leading=10.2, textColor=colors.HexColor("#E9F3F7"),
))
styles.add(ParagraphStyle(
    name="AnnexQ", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=9.2, leading=12.5, textColor=NAVY, spaceBefore=7, spaceAfter=2,
))


def footer(canvas, doc):
    """Cabecera y pie sobrios para páginas interiores."""
    page = canvas.getPageNumber()
    if page == 1:
        return
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(TEAL)
    canvas.drawString(18 * mm, height - 10.5 * mm, "S01 · PAGATU ORDEN MS")
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 18 * mm, height - 10.5 * mm, "Aldo Calla Ticona")
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.drawString(18 * mm, 8.5 * mm, "Construcción de un servicio base para un sistema distribuido")
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, f"{page:02d}")
    canvas.restoreState()


def cover(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.circle(width + 18 * mm, height - 35 * mm, 58 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.circle(width - 8 * mm, height - 23 * mm, 30 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(20 * mm, height - 49 * mm, 20 * mm, 2.2 * mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.HexColor("#BBDCE7"))
    canvas.drawString(20 * mm, height - 26 * mm, "INGENIERÍA DE SOFTWARE · EVIDENCIA TÉCNICA")
    canvas.setFillColor(colors.HexColor("#203C54"))
    canvas.roundRect(20 * mm, 24 * mm, width - 40 * mm, 54 * mm, 4 * mm, fill=1, stroke=0)
    canvas.restoreState()


def p(text, style="BodyS01"):
    return Paragraph(text, styles[style])


def section(number, title):
    return Paragraph(f'<font color="#168C8C">{number:02d}</font>  {title}', styles["Section"])


def evidence(filename, max_width=174 * mm, max_height=112 * mm):
    img = Image(str(ASSETS / filename))
    ratio = min(max_width / img.imageWidth, max_height / img.imageHeight)
    img.drawWidth = img.imageWidth * ratio
    img.drawHeight = img.imageHeight * ratio
    img.hAlign = "CENTER"
    return img


def caption(number, text):
    return p(f"Evidencia {number}. {text}", "Caption")


def info_cards():
    data = [
        [p("ESTUDIANTE", "Label"), p("EQUIPO", "Label"), p("ENTREGA", "Label")],
        [p("Aldo Calla Ticona", "CoverValue"), p("Sin grupo", "CoverValue"), p("S01 · 27/08/2026", "CoverValue")],
        [p("SERVICIO", "Label"), p("STACK", "Label"), p("REPOSITORIO", "Label")],
        [p("pagatu-orden-ms", "CoverValue"), p("Java 21 · Spring Boot 4 · PostgreSQL 16", "CoverValue"), p("github.com/Aldo-Ct/Pagalotu", "CoverValue")],
    ]
    table = Table(data, colWidths=[52 * mm, 52 * mm, 54 * mm], rowHeights=[7 * mm, 9 * mm, 7 * mm, 11 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#203C54")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#426178")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#426178")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def styled_table(rows, widths, header=True):
    converted = []
    for row_index, row in enumerate(rows):
        style_name = "TableHeader" if header and row_index == 0 else "Small"
        converted.append([p(str(cell), style_name) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER]),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    table.setStyle(TableStyle(commands))
    return table


def callout(title, text):
    table = Table([[p(title, "Label"), p(text, "Small")]], colWidths=[31 * mm, 127 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CYAN),
        ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def code_block(lines):
    body = "<br/>".join(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for line in lines)
    table = Table([[Paragraph(body, styles["CodeS01"])]], colWidths=[158 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=20 * mm, bottomMargin=18 * mm,
        title="S01 - Construcción de un servicio base para un sistema distribuido",
        author="Aldo Calla Ticona",
        subject="Evidencia técnica de pagatu-orden-ms",
    )

    story = []

    # Portada
    story.extend([
        Spacer(1, 47 * mm),
        p("S01", "S01Title"),
        p("Construcción de un servicio base<br/>para un sistema distribuido", "S01Title"),
        Spacer(1, 5 * mm),
        p("Microservicio de órdenes · Spring Boot · PostgreSQL · Flyway · OpenAPI", "S01Subtitle"),
        Spacer(1, 61 * mm),
        info_cards(),
        Spacer(1, 9 * mm),
        p("Informe de implementación individual con evidencia de arquitectura por capas, persistencia, contrato REST, observabilidad y escalamiento horizontal.", "S01Subtitle"),
        PageBreak(),
    ])

    # 1
    story.extend([
        section(1, "Microservicio delimitado por dominio"),
        p("<b>pagatu-orden-ms</b> gestiona exclusivamente órdenes y sus detalles: cliente asociado, estado, comprobante, pago, total, productos, cantidades y precios registrados. No administra categorías, productos ni clientes; conserva sus identificadores porque esos datos pertenecen a otros dominios."),
        callout("LÍMITE", "La lógica de Orden permanece independiente de Catálogo y Cliente. Esta separación reduce acoplamiento y permite evolucionar cada servicio por separado."),
        Spacer(1, 6 * mm),
        evidence("01_dominio_flyway.png", max_height=104 * mm),
        caption(1, "Capas controller, service, repository, entity, dto, mapper, exception y filter, junto con la migración versionada V1."),
        p("<b>Resultado.</b> Las responsabilidades están separadas y el esquema se versiona como parte del propio microservicio."),
        PageBreak(),
    ])

    # 2a
    story.extend([
        section(2, "Persistencia reproducible: runtime y migración"),
        p("El ambiente DEV usa PostgreSQL 16 en Docker y el servicio se construye con Maven Wrapper sobre Java 21. Flyway valida la migración antes de que la aplicación acepte tráfico."),
        evidence("05_maven_arranque.png", max_height=112 * mm),
        caption(2, "Maven Wrapper 3.9.16, Java 21, migración Flyway aplicada, proceso en 8080 y estado Health/DB UP."),
        styled_table([
            ["Componente", "Verificación"],
            ["Java / Maven", "Java 21 y Maven Wrapper 3.9.16"],
            ["Flyway", "V1 create orden tables aplicada con éxito"],
            ["Spring Boot", "Proceso Java escuchando en 8080"],
            ["Actuator", "status UP y conexión PostgreSQL UP"],
        ], [42 * mm, 116 * mm]),
        PageBreak(),
    ])

    # 2b
    story.extend([
        section(2, "Persistencia reproducible: datos"),
        p("La consulta directa con <b>psql</b> confirma las tablas creadas por Flyway y demuestra que los datos escritos por la API permanecen en PostgreSQL."),
        evidence("02_postgresql.png", max_height=118 * mm),
        caption(3, "Tablas ordenes, orden_detalles y flyway_schema_history; orden 2 persistida con total 60.00 y tres unidades a 20.00."),
        callout("TRAZABILIDAD", "La evidencia enlaza migración, esquema y registro persistido. No se depende de memoria local ni de datos simulados."),
        PageBreak(),
    ])

    # 3
    endpoint_rows = [
        ["Operación", "Endpoint", "Resultado"],
        ["Crear", "POST /api/v1/ordenes", "HTTP 201"],
        ["Listar", "GET /api/v1/ordenes", "HTTP 200"],
        ["Obtener", "GET /api/v1/ordenes/2", "HTTP 200"],
        ["Actualizar", "PUT /api/v1/ordenes/2", "HTTP 200"],
        ["Eliminar", "DELETE /api/v1/ordenes/{id}", "HTTP 204"],
        ["Validación", "POST con datos incompletos", "HTTP 400"],
        ["Inexistente", "GET /api/v1/ordenes/99999", "HTTP 404"],
    ]
    story.extend([
        section(3, "API REST funcional y documentada"),
        p("El recurso principal utiliza <b>/api/v1/ordenes</b>, ofrece CRUD completo y expone contrato OpenAPI. Las pruebas se ejecutaron desde shell."),
        styled_table(endpoint_rows, [31 * mm, 92 * mm, 35 * mm]),
        Spacer(1, 5 * mm),
        evidence("03_crud_swagger.png", max_height=91 * mm),
        caption(4, "Lectura del registro actualizado, validación HTTP 400, recurso inexistente HTTP 404 y rutas publicadas por OpenAPI."),
        PageBreak(),
    ])

    # 4
    story.extend([
        section(4, "Ejecución y escalamiento horizontal"),
        p("Se ejecutaron simultáneamente dos instancias del mismo artefacto: 8080 y 8081. Ambas comparten PostgreSQL DEV y responden de forma independiente."),
        evidence("04_escalamiento.png", max_height=84 * mm),
        caption(5, "Dos procesos Java independientes, misma API y puertos distintos; health, base de datos y métricas disponibles."),
        styled_table([
            ["Aspecto", "Instancia 1", "Instancia 2"],
            ["Puerto", "8080", "8081 por argumento"],
            ["Base de datos", "PostgreSQL DEV", "PostgreSQL DEV compartida"],
            ["/saludo", "HTTP 200", "HTTP 200"],
            ["/actuator/health", "UP · DB UP", "UP · DB UP"],
        ], [46 * mm, 55 * mm, 57 * mm]),
        Spacer(1, 5 * mm),
        callout("STATELESS", "Cualquier instancia puede atender una solicitud sin memoria local previa. Un Gateway o balanceador podrá distribuir tráfico entre copias equivalentes."),
        PageBreak(),
    ])

    # 5
    story.extend([
        section(5, "Documentación técnica y reproducción"),
        p("El README documenta requisitos, Docker Compose, Maven Wrapper, Swagger, Actuator, pruebas CRUD, consultas psql y la segunda instancia."),
        p("Arranque del ambiente DEV", "Subsection"),
        code_block([
            "cd Services/pagatu-orden-ms",
            "docker compose -f compose-dev.yml up -d",
            "./mvnw spring-boot:run",
        ]),
        p("Segunda instancia y verificación", "Subsection"),
        code_block([
            "./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8081",
            "curl http://localhost:8080/actuator/health",
            "curl http://localhost:8081/actuator/health",
            "curl http://localhost:8080/api/v1/ordenes",
        ]),
        p("Hallazgo técnico", "Subsection"),
        p("En el primer arranque apareció <b>Unable to obtain connection from database</b>. PostgreSQL aún no estaba disponible en localhost:15434. Se inició el contenedor DEV, se verificó la conexión y Flyway aplicó V1 correctamente."),
        p("Al levantar 8081, LiveReload avisó que su puerto auxiliar estaba ocupado. El aviso no detuvo Tomcat ni afectó los endpoints; permitió diferenciar el puerto auxiliar de desarrollo del puerto HTTP principal."),
        callout("ALCANCE", "La ejecución PROD local es opcional en la guía y no es necesaria para alcanzar el nivel A; la evidencia se concentra en DEV reproducible."),
        PageBreak(),
    ])

    # Conclusión
    story.extend([
        section(6, "Reflexión técnica y conclusión"),
        p("<b>Aprendizajes principales</b>", "Subsection"),
        styled_table([
            ["Principio", "Aplicación en Pagatu"],
            ["Reproducibilidad", "Maven Wrapper y Docker Compose eliminan configuraciones manuales ocultas."],
            ["Persistencia", "Flyway versiona el esquema y PostgreSQL conserva datos fuera del proceso Java."],
            ["Desacoplamiento", "Orden conserva identificadores de recursos que pertenecen a otros dominios."],
            ["Escalabilidad", "El puerto se externaliza y las instancias se mantienen stateless."],
            ["Observabilidad", "Actuator permite verificar salud, base de datos y métricas."],
        ], [43 * mm, 115 * mm]),
        Spacer(1, 8 * mm),
        callout("CONCLUSIÓN", "pagatu-orden-ms cumple el servicio base de S01: dominio delimitado, persistencia versionada, CRUD documentado, manejo de errores, observabilidad y ejecución horizontal comprobada."),
        Spacer(1, 9 * mm),
        p("La solución queda preparada para integrarse posteriormente con Config Server, Service Discovery, API Gateway y balanceo de carga, sin alterar el núcleo del dominio implementado."),
        PageBreak(),
    ])

    # Anexo
    annex = [
        ("1. ¿Cuál es el aprendizaje más importante?", "Que los microservicios permiten dividir responsabilidades y evitar que todo el sistema dependa de un único componente. Si un servicio falla, los demás pueden continuar funcionando."),
        ("2. ¿Qué punto resultó más confuso?", "La instalación de dependencias y la creación del proyecto en VS Code y Spring Initializr, porque antes trabajaba en IntelliJ y ese proceso me resultaba más sencillo."),
        ("3. Pregunta para la siguiente clase", "¿Cuál es la forma recomendada de instalar y gestionar dependencias de Spring Boot desde VS Code para evitar errores de compatibilidad?"),
        ("4. Nivel de comprensión", "Más o menos. Entendí la idea general, pero todavía tengo dudas."),
        ("5. ¿Cómo pueden ayudarme a comprender mejor?", "Repasando paso a paso la creación del proyecto y la selección o instalación de dependencias en VS Code."),
        ("6. Autoevaluación", "Comprometido. Sé que podría haberme esforzado un poco más."),
        ("7. Satisfacción con la clase", "7 de 10."),
    ]
    story.append(section(7, "Anexo · Feedback de la sesión"))
    story.append(p("Respuestas de autoevaluación y retroalimentación correspondientes a la sesión S01."))
    for question, answer in annex:
        story.append(p(question, "AnnexQ"))
        story.append(p(answer))
    story.extend([
        Spacer(1, 7 * mm),
        callout("ENTREGA", "Documento generado a partir de evidencia ejecutada localmente el 27/08/2026. Repositorio: github.com/Aldo-Ct/Pagalotu"),
    ])

    doc.build(story, onFirstPage=cover, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
