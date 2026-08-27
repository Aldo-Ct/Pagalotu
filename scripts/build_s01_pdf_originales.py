#!/usr/bin/env python3
"""Genera el informe S01 usando las capturas originales completas y sin recorte."""

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "capturas" / "originales_s01"
OUTPUT = ROOT / "output" / "pdf" / "S01_SinGrupo_CallaAldo.pdf"
PAGE_W, PAGE_H = landscape(A4)

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

BODY = ParagraphStyle(
    "Body", fontName="Helvetica", fontSize=9.5, leading=13.5,
    textColor=INK, alignment=TA_LEFT,
)
SMALL = ParagraphStyle(
    "Small", fontName="Helvetica", fontSize=8.2, leading=11.2,
    textColor=INK, alignment=TA_LEFT,
)
HEADER_CELL = ParagraphStyle(
    "HeaderCell", fontName="Helvetica-Bold", fontSize=8.4, leading=11.2,
    textColor=WHITE, alignment=TA_LEFT,
)
WHITE_BODY = ParagraphStyle(
    "WhiteBody", fontName="Helvetica", fontSize=9.5, leading=13.5,
    textColor=WHITE, alignment=TA_LEFT,
)
CODE = ParagraphStyle(
    "Code", fontName="Courier", fontSize=8.2, leading=11.2,
    textColor=colors.HexColor("#E8F3F7"), alignment=TA_LEFT,
)


EVIDENCE = [
    ("05_dominio.png", "01", "Dominio y arquitectura por capas",
     "Estructura implementada para el dominio Orden y migración versionada con Flyway."),
    ("04_runtime_verificado.png", "02", "Runtime DEV verificado",
     "Java 21, Maven Wrapper, Flyway, proceso Spring Boot y estado de la base de datos."),
    ("01_runtime_general.png", "03", "Runtime completo en el entorno de trabajo",
     "Vista completa de VS Code y la terminal con la validación del ambiente DEV."),
    ("03_postgresql.png", "04", "Persistencia en PostgreSQL",
     "Tablas creadas por Flyway y registros persistidos en ordenes y orden_detalles."),
    ("02_api_rest.png", "05", "CRUD y contrato OpenAPI",
     "Respuesta de la API, validación HTTP 400, recurso HTTP 404 y rutas publicadas."),
    ("10_escalamiento.png", "06", "Escalamiento horizontal",
     "Dos procesos Java independientes en 8080 y 8081 compartiendo PostgreSQL DEV."),
    ("07_arranque_8080.png", "07", "Arranque de la instancia 8080",
     "Spring Boot inicia la primera instancia y Tomcat queda asociado al puerto 8080."),
    ("06_arranque_8081.png", "08", "Arranque de la instancia 8081",
     "El mismo artefacto se ejecuta como segunda instancia mediante server.port=8081."),
    ("09_arranque_8080_repeticion.png", "09", "Evidencia complementaria de 8080",
     "Vista original adicional del arranque de la primera instancia, conservada sin cambios."),
    ("08_arranque_8081_repeticion.png", "10", "Evidencia complementaria de 8081",
     "Vista original adicional del arranque de la segunda instancia, conservada sin cambios."),
]


def para(text, style=BODY):
    return Paragraph(text, style)


def draw_paragraph(pdf, text, x, y_top, width, style=BODY):
    paragraph = para(text, style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(pdf, x, y_top - height)
    return y_top - height


def draw_header(pdf, title, section, page_number):
    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.7)
    pdf.line(18 * mm, PAGE_H - 14 * mm, PAGE_W - 18 * mm, PAGE_H - 14 * mm)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 7.6)
    pdf.drawString(18 * mm, PAGE_H - 10.5 * mm, "S01 - PAGATU ORDEN MS")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.4)
    pdf.drawRightString(PAGE_W - 18 * mm, PAGE_H - 10.5 * mm, "Aldo Calla Ticona")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(18 * mm, PAGE_H - 27 * mm, section)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(34 * mm, PAGE_H - 27 * mm, title)
    draw_footer(pdf, page_number)


def draw_footer(pdf, page_number):
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.7)
    pdf.line(18 * mm, 13 * mm, PAGE_W - 18 * mm, 13 * mm)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.3)
    pdf.drawString(18 * mm, 8.5 * mm, "Construcción de un servicio base para un sistema distribuido")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawRightString(PAGE_W - 18 * mm, 8.5 * mm, f"{page_number:02d}")


def draw_cover(pdf):
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(BLUE)
    pdf.circle(PAGE_W - 8 * mm, PAGE_H - 18 * mm, 55 * mm, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.circle(PAGE_W + 3 * mm, PAGE_H - 2 * mm, 34 * mm, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(22 * mm, PAGE_H - 52 * mm, 22 * mm, 2.3 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#BBDCE7"))
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(22 * mm, PAGE_H - 29 * mm, "INGENIERÍA DE SOFTWARE - EVIDENCIA TÉCNICA")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(22 * mm, PAGE_H - 76 * mm, "S01")
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(22 * mm, PAGE_H - 93 * mm, "Construcción de un servicio base")
    pdf.drawString(22 * mm, PAGE_H - 108 * mm, "para un sistema distribuido")
    pdf.setFillColor(colors.HexColor("#D9EEF5"))
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(22 * mm, PAGE_H - 124 * mm, "Microservicio de órdenes - Spring Boot - PostgreSQL - Flyway - OpenAPI")

    pdf.setFillColor(colors.HexColor("#203C54"))
    pdf.roundRect(22 * mm, 28 * mm, PAGE_W - 44 * mm, 45 * mm, 4 * mm, fill=1, stroke=0)
    labels = [
        ("ESTUDIANTE", "Aldo Calla Ticona"),
        ("EQUIPO", "Sin grupo"),
        ("SERVICIO", "pagatu-orden-ms"),
        ("ENTREGA", "S01 - 27/08/2026"),
    ]
    column_w = (PAGE_W - 54 * mm) / 4
    for index, (label, value) in enumerate(labels):
        x = 28 * mm + index * column_w
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 7.7)
        pdf.drawString(x, 59 * mm, label)
        pdf.setFillColor(WHITE)
        pdf.setFont("Helvetica", 9.3)
        pdf.drawString(x, 47 * mm, value)
    pdf.setFillColor(colors.HexColor("#BBDCE7"))
    pdf.setFont("Helvetica", 8)
    pdf.drawString(28 * mm, 34 * mm, "Informe regenerado con 10 capturas originales completas, sin recorte ni reconstrucción.")


def styled_table(rows, widths):
    converted = []
    for row_index, row in enumerate(rows):
        style = HEADER_CELL if row_index == 0 else SMALL
        converted.append([para(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER]),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def draw_summary(pdf, page_number):
    draw_header(pdf, "Resumen de la implementación", "00", page_number)
    x = 18 * mm
    width = PAGE_W - 36 * mm
    y = PAGE_H - 38 * mm
    y = draw_paragraph(
        pdf,
        "<b>pagatu-orden-ms</b> delimita el dominio de órdenes, persiste datos en PostgreSQL mediante migraciones Flyway, expone un CRUD REST documentado con OpenAPI y puede ejecutarse como dos instancias stateless en puertos distintos.",
        x, y, width,
    ) - 8 * mm
    rows = [
        ["Criterio", "Implementación", "Evidencia"],
        ["Dominio", "Capas controller, service, repository, entity, dto, mapper, exception y filter.", "Evidencia 01"],
        ["Persistencia", "PostgreSQL 16, migración V1 y registros persistidos.", "Evidencias 02-04"],
        ["API REST", "CRUD, validación HTTP 400, recurso HTTP 404 y OpenAPI.", "Evidencia 05"],
        ["Escalamiento", "Instancias independientes en 8080 y 8081 con PostgreSQL compartida.", "Evidencias 06-10"],
        ["Reproducibilidad", "Java 21, Maven Wrapper, Docker Compose y Actuator.", "Documentación"],
    ]
    table = styled_table(rows, [45 * mm, 164 * mm, 48 * mm])
    _, table_h = table.wrap(width, PAGE_H)
    table.drawOn(pdf, x, y - table_h)
    y = y - table_h - 10 * mm
    pdf.setFillColor(CYAN)
    pdf.roundRect(x, y - 31 * mm, width, 31 * mm, 3 * mm, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x + 8 * mm, y - 11 * mm, "ALCANCE VERIFICADO")
    draw_paragraph(
        pdf,
        "Las capturas muestran el ambiente real de trabajo, las herramientas, la base de datos, los endpoints y ambos procesos Java. Cada imagen se incorpora completa y conserva su relación de aspecto original.",
        x + 49 * mm, y - 7 * mm, width - 58 * mm, SMALL,
    )


def draw_evidence_page(pdf, source_name, number, title, caption_text, page_number):
    draw_header(pdf, title, number, page_number)
    source = CAPTURES / source_name
    with PILImage.open(source) as image:
        pixel_w, pixel_h = image.size

    left = 18 * mm
    right = PAGE_W - 18 * mm
    bottom = 26 * mm
    top = PAGE_H - 39 * mm
    available_w = right - left
    available_h = top - bottom
    scale = min(available_w / pixel_w, available_h / pixel_h)
    draw_w = pixel_w * scale
    draw_h = pixel_h * scale
    image_x = left + (available_w - draw_w) / 2
    image_y = bottom + (available_h - draw_h) / 2

    pdf.setFillColor(PAPER)
    pdf.roundRect(left, bottom, available_w, available_h, 3 * mm, fill=1, stroke=0)
    pdf.setStrokeColor(colors.HexColor("#BFCBD4"))
    pdf.setLineWidth(0.7)
    pdf.rect(image_x - 1, image_y - 1, draw_w + 2, draw_h + 2, fill=0, stroke=1)
    pdf.drawImage(str(source), image_x, image_y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(left, 18.5 * mm, f"Evidencia {number}. {caption_text}")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.2)
    pdf.drawRightString(right, 18.5 * mm, f"Original {pixel_w} x {pixel_h} px - imagen completa - sin recorte")


def draw_reproduction(pdf, page_number):
    draw_header(pdf, "Documentación técnica y reproducción", "11", page_number)
    x = 18 * mm
    y = PAGE_H - 40 * mm
    width = PAGE_W - 36 * mm
    y = draw_paragraph(pdf, "El ambiente DEV se reproduce con Docker Compose y Maven Wrapper. Los puertos se externalizan para evitar acoplamiento y permitir copias equivalentes del servicio.", x, y, width) - 7 * mm

    pdf.setFillColor(NAVY)
    pdf.roundRect(x, y - 42 * mm, width, 42 * mm, 3 * mm, fill=1, stroke=0)
    commands = (
        "cd Services/pagatu-orden-ms<br/>"
        "docker compose -f compose-dev.yml up -d<br/>"
        "./mvnw clean package -DskipTests<br/>"
        "java -jar target/pagatu-orden-ms-0.0.1-SNAPSHOT.jar --server.port=8080<br/>"
        "java -jar target/pagatu-orden-ms-0.0.1-SNAPSHOT.jar --server.port=8081"
    )
    draw_paragraph(pdf, commands, x + 8 * mm, y - 8 * mm, width - 16 * mm, CODE)
    y -= 53 * mm

    rows = [
        ["Verificación", "URL / comando", "Resultado"],
        ["Health 8080", "http://localhost:8080/actuator/health", "UP - DB UP"],
        ["Health 8081", "http://localhost:8081/actuator/health", "UP - DB UP"],
        ["Swagger", "http://localhost:8080/swagger-ui/index.html", "HTTP 200"],
        ["Órdenes", "http://localhost:8080/api/v1/ordenes", "HTTP 200"],
    ]
    table = styled_table(rows, [52 * mm, 153 * mm, 52 * mm])
    _, table_h = table.wrap(width, PAGE_H)
    table.drawOn(pdf, x, y - table_h)
    y -= table_h + 10 * mm

    pdf.setFillColor(CYAN)
    pdf.roundRect(x, y - 34 * mm, width, 34 * mm, 3 * mm, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x + 8 * mm, y - 11 * mm, "HALLAZGO TÉCNICO")
    draw_paragraph(
        pdf,
        "El primer fallo de la segunda instancia no correspondía al puerto 8081: Spring no encontraba OrdenMapper durante una compilación concurrente. Un clean package produjo un JAR estable y permitió ejecutar 8080 y 8081 de forma independiente.",
        x + 49 * mm, y - 7 * mm, width - 58 * mm, SMALL,
    )


def draw_conclusion(pdf, page_number):
    draw_header(pdf, "Reflexión técnica y conclusión", "12", page_number)
    x = 18 * mm
    y = PAGE_H - 40 * mm
    width = PAGE_W - 36 * mm
    rows = [
        ["Principio", "Aplicación en Pagatu"],
        ["Reproducibilidad", "Maven Wrapper y Docker Compose eliminan configuraciones manuales ocultas."],
        ["Persistencia", "Flyway versiona el esquema y PostgreSQL conserva los datos fuera del proceso Java."],
        ["Desacoplamiento", "Orden conserva identificadores de recursos pertenecientes a otros dominios."],
        ["Escalabilidad", "El puerto se externaliza y las instancias permanecen stateless."],
        ["Observabilidad", "Actuator verifica salud, base de datos y métricas."],
    ]
    table = styled_table(rows, [58 * mm, 199 * mm])
    _, table_h = table.wrap(width, PAGE_H)
    table.drawOn(pdf, x, y - table_h)
    y -= table_h + 11 * mm

    pdf.setFillColor(CYAN)
    pdf.roundRect(x, y - 35 * mm, width, 35 * mm, 3 * mm, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x + 8 * mm, y - 12 * mm, "CONCLUSIÓN")
    draw_paragraph(
        pdf,
        "pagatu-orden-ms cumple el servicio base de S01: dominio delimitado, persistencia versionada, CRUD documentado, manejo de errores, observabilidad y ejecución horizontal comprobada. La solución queda preparada para integrarse con Config Server, Service Discovery, API Gateway y balanceo de carga.",
        x + 41 * mm, y - 8 * mm, width - 50 * mm, SMALL,
    )
    y -= 48 * mm
    draw_paragraph(pdf, "<b>Repositorio:</b> https://github.com/Aldo-Ct/Pagalotu", x, y, width)
    draw_paragraph(pdf, "<b>Archivos originales:</b> capturas/originales_s01/", x, y - 8 * mm, width)


def draw_feedback(pdf, page_number):
    draw_header(pdf, "Anexo - Feedback de la sesión", "13", page_number)
    x = 18 * mm
    y = PAGE_H - 39 * mm
    width = PAGE_W - 36 * mm
    feedback = [
        ("1. Aprendizaje más importante", "Los microservicios permiten dividir responsabilidades y evitar que todo el sistema dependa de un único componente."),
        ("2. Punto más confuso", "La instalación de dependencias y la creación del proyecto en VS Code y Spring Initializr."),
        ("3. Pregunta para la siguiente clase", "¿Cuál es la forma recomendada de gestionar dependencias de Spring Boot desde VS Code para evitar incompatibilidades?"),
        ("4. Nivel de comprensión", "Más o menos. Entendí la idea general, pero todavía tengo dudas."),
        ("5. Apoyo solicitado", "Repasar paso a paso la creación del proyecto y la selección o instalación de dependencias en VS Code."),
        ("6. Autoevaluación", "Comprometido. Sé que podría haberme esforzado un poco más."),
        ("7. Satisfacción", "7 de 10."),
    ]
    for question, answer in feedback:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 9.2)
        pdf.drawString(x, y, question)
        y -= 5 * mm
        y = draw_paragraph(pdf, answer, x, y, width, SMALL) - 4.5 * mm


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(
        str(OUTPUT), pagesize=(PAGE_W, PAGE_H),
        pageCompression=1,
    )
    pdf.setTitle("S01 - Construcción de un servicio base para un sistema distribuido")
    pdf.setAuthor("Aldo Calla Ticona")
    pdf.setSubject("Evidencia técnica de pagatu-orden-ms con capturas originales completas")

    draw_cover(pdf)
    pdf.showPage()
    page_number = 2

    draw_summary(pdf, page_number)
    pdf.showPage()
    page_number += 1

    for source_name, number, title, caption_text in EVIDENCE:
        draw_evidence_page(pdf, source_name, number, title, caption_text, page_number)
        pdf.showPage()
        page_number += 1

    draw_reproduction(pdf, page_number)
    pdf.showPage()
    page_number += 1
    draw_conclusion(pdf, page_number)
    pdf.showPage()
    page_number += 1
    draw_feedback(pdf, page_number)
    pdf.showPage()

    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
