from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "S02_SinGrupo_CallaAldo.pdf"
SHOTS = ROOT / "capturas" / "originales_s02"
PAGE_W, PAGE_H = landscape(A4)

NAVY = colors.HexColor("#10243E")
BLUE = colors.HexColor("#1479C9")
CYAN = colors.HexColor("#29B8C9")
GREEN = colors.HexColor("#36A269")
LIGHT = colors.HexColor("#F3F7FA")
MID = colors.HexColor("#D8E3EC")
TEXT = colors.HexColor("#23384D")
MUTED = colors.HexColor("#617487")
WHITE = colors.white

styles = getSampleStyleSheet()
BODY = ParagraphStyle("BodyS02", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=14, textColor=TEXT)
SMALL = ParagraphStyle("SmallS02", parent=BODY, fontSize=8.8, leading=12)
TITLE = ParagraphStyle("TitleS02", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=26, leading=31, textColor=WHITE)
SUB = ParagraphStyle("SubS02", parent=BODY, fontSize=12, leading=17, textColor=WHITE)
H1 = ParagraphStyle("H1S02", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=NAVY)
H2 = ParagraphStyle("H2S02", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=BLUE)
CENTER = ParagraphStyle("CenterS02", parent=BODY, alignment=TA_CENTER)


def draw_header(c, section, title):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 25 * mm, PAGE_W, 25 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(0, PAGE_H - 25 * mm, 7 * mm, 25 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(14 * mm, PAGE_H - 9 * mm, section.upper())
    c.setFont("Helvetica-Bold", 18)
    c.drawString(14 * mm, PAGE_H - 18 * mm, title)


def footer(c, page_num):
    c.setStrokeColor(MID)
    c.line(14 * mm, 12 * mm, PAGE_W - 14 * mm, 12 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(14 * mm, 7 * mm, "S02 - Configuracion centralizada de ambientes | Aldo Calla Ticona")
    c.drawRightString(PAGE_W - 14 * mm, 7 * mm, f"Pagina {page_num}")


def para(c, text, style, x, y_top, width, height=60 * mm):
    p = Paragraph(text, style)
    w, h = p.wrap(width, height)
    p.drawOn(c, x, y_top - h)
    return h


def pill(c, x, y, text, color=GREEN):
    w = stringWidth(text, "Helvetica-Bold", 8) + 8 * mm
    c.setFillColor(color)
    c.roundRect(x, y, w, 7 * mm, 3.5 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, y + 2.2 * mm, text)
    return w


def evidence_page(c, page_num, code, title, filename, caption, finding):
    draw_header(c, code, title)
    img = ImageReader(str(SHOTS / filename))
    iw, ih = img.getSize()
    x0, x1 = 14 * mm, PAGE_W - 14 * mm
    y0, y1 = 33 * mm, PAGE_H - 31 * mm
    max_w, max_h = x1 - x0, y1 - y0
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    ix, iy = x0 + (max_w - dw) / 2, y0 + (max_h - dh) / 2
    c.setFillColor(colors.HexColor("#E7EEF4"))
    c.roundRect(ix - 1.5 * mm, iy - 1.5 * mm, dw + 3 * mm, dh + 3 * mm, 2.5 * mm, fill=1, stroke=0)
    c.drawImage(img, ix, iy, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
    c.setFillColor(LIGHT)
    c.roundRect(14 * mm, 16 * mm, PAGE_W - 28 * mm, 13 * mm, 2.5 * mm, fill=1, stroke=0)
    para(c, f"<b>Evidencia:</b> {caption} &nbsp;&nbsp; <font color='#1479C9'><b>Hallazgo:</b></font> {finding}", SMALL, 18 * mm, 26 * mm, PAGE_W - 36 * mm, 12 * mm)
    footer(c, page_num)
    c.showPage()


def make_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("S02 - Configuracion centralizada de ambientes")
    c.setAuthor("Aldo Calla Ticona")

    # 1. Portada
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.circle(PAGE_W - 28 * mm, PAGE_H - 26 * mm, 42 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.circle(PAGE_W - 5 * mm, 8 * mm, 36 * mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#173653"))
    c.roundRect(16 * mm, 18 * mm, PAGE_W - 32 * mm, PAGE_H - 36 * mm, 6 * mm, fill=1, stroke=0)
    pill(c, 28 * mm, PAGE_H - 48 * mm, "SESION 02")
    para(c, "Gestion centralizada de<br/>configuracion y ambientes", TITLE, 28 * mm, PAGE_H - 62 * mm, 150 * mm, 55 * mm)
    para(c, "Config Server, perfiles DEV/PROD y Config Client aplicados a los microservicios Pagatu.", SUB, 28 * mm, PAGE_H - 123 * mm, 155 * mm, 30 * mm)
    info = [
        ["Estudiante", "Aldo Calla Ticona"],
        ["Equipo", "Sin grupo - trabajo individual"],
        ["Rol / aporte", "Implementacion y verificacion integral"],
        ["Repositorio", "github.com/Aldo-Ct/Pagalotu"],
        ["Fecha", "27 de agosto de 2026"],
    ]
    t = Table(info, colWidths=[33 * mm, 105 * mm], rowHeights=9 * mm)
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#456176")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    t.wrapOn(c, 138 * mm, 50 * mm)
    t.drawOn(c, 28 * mm, 31 * mm)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(PAGE_W - 28 * mm, 28 * mm, "PAGATU / S02")
    c.showPage()

    # 2. Resumen y arquitectura
    draw_header(c, "Resumen", "Objetivo, alcance y arquitectura verificada")
    para(c, "<b>Resultado:</b> se centralizaron las propiedades por ambiente y el microservicio de ordenes consume su configuracion desde Config Server. Las pruebas demuestran salud, carga de perfiles, acceso a PostgreSQL y funcionamiento del endpoint REST.", BODY, 16 * mm, PAGE_H - 34 * mm, PAGE_W - 32 * mm, 25 * mm)
    y = 92 * mm
    boxes = [
        (18 * mm, "CONFIG REPO", "orden-ms-dev.yml<br/>orden-ms-prod.yml<br/>catalogo dev/prod", BLUE),
        (108 * mm, "CONFIG SERVER", "Spring Cloud Config<br/>localhost:18888<br/>actuator: UP", CYAN),
        (198 * mm, "CONFIG CLIENT", "orden-ms<br/>perfil: dev<br/>puerto: 8080", GREEN),
    ]
    for x, head, body, color in boxes:
        c.setFillColor(LIGHT)
        c.roundRect(x, y, 72 * mm, 45 * mm, 4 * mm, fill=1, stroke=0)
        c.setFillColor(color)
        c.roundRect(x, y + 34 * mm, 72 * mm, 11 * mm, 4 * mm, fill=1, stroke=0)
        c.rect(x, y + 34 * mm, 72 * mm, 5 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 10); c.drawString(x + 5 * mm, y + 38 * mm, head)
        para(c, body, CENTER, x + 5 * mm, y + 28 * mm, 62 * mm, 25 * mm)
    c.setStrokeColor(MUTED); c.setLineWidth(1.5)
    c.line(90 * mm, y + 22 * mm, 105 * mm, y + 22 * mm); c.line(180 * mm, y + 22 * mm, 195 * mm, y + 22 * mm)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 14); c.drawString(96 * mm, y + 19 * mm, ">") ; c.drawString(186 * mm, y + 19 * mm, ">")
    rows = [
        ["Criterio", "Resultado", "Evidencia"],
        ["Config Server disponible", "Cumplido", "Health UP en :18888"],
        ["Perfiles orden-ms DEV/PROD", "Cumplido", "PropertySources diferentes"],
        ["orden-ms como Config Client", "Cumplido", "Carga remota y arranque en 8080"],
        ["Funcionamiento con datos", "Cumplido", "DB UP y GET /api/v1/ordenes"],
        ["Comparacion catalogo DEV/PROD", "Cumplido", "Valores reales externalizados"],
    ]
    table = Table(rows, colWidths=[72 * mm, 35 * mm, 140 * mm], rowHeights=[8 * mm] + [9 * mm] * 5)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.7), ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, MID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    table.wrapOn(c, PAGE_W - 36 * mm, 55 * mm); table.drawOn(c, 18 * mm, 27 * mm)
    footer(c, 2); c.showPage()

    evidence_page(c, 3, "Evidencia 1", "Config Server operativo", "01_config_server_up.png", "respuesta completa de /actuator/health, con fecha, hora y usuario visibles.", "el servidor central responde UP en el puerto 18888.")
    evidence_page(c, 4, "Evidencia 2", "Perfiles externos de orden-ms", "02_perfiles_orden.png", "consulta de /orden-ms/dev y /orden-ms/prod sobre el repositorio de configuracion.", "DEV usa valores locales; PROD delega puerto y base de datos a variables de entorno.")
    evidence_page(c, 5, "Evidencia 3", "orden-ms conectado como Config Client", "03_config_client.png", "logs de arranque que muestran la consulta a http://localhost:18888 y la localizacion del perfil dev.", "el arranque vigente termina correctamente en el puerto 8080.")
    evidence_page(c, 6, "Evidencia 4", "Servicio funcional con configuracion externa", "04_health_crud.png", "health del microservicio y GET /api/v1/ordenes ejecutados contra la instancia configurada externamente.", "aplicacion y PostgreSQL responden UP; el endpoint devuelve datos persistidos.")
    evidence_page(c, 7, "Evidencia 5", "Comparacion real de catalogo DEV y PROD", "05_comparacion_catalogo.png", "valores servidos por los perfiles pagatu-catalogo-ms-dev y pagatu-catalogo-ms-prod.", "se externalizaron URL JDBC, SQL visible y detalle de health segun el ambiente.")

    # 8. Analisis
    draw_header(c, "Analisis", "Separacion entre codigo y configuracion")
    para(c, "<b>Principio aplicado.</b> El codigo define el comportamiento del servicio; la configuracion define como ese mismo artefacto se conecta y se comporta en cada ambiente. Por eso el microservicio conserva solo su identidad, perfil e importacion del Config Server, mientras los puertos, URLs JDBC, logging, Actuator y Swagger se mantienen en el repositorio central.", BODY, 16 * mm, PAGE_H - 35 * mm, PAGE_W - 32 * mm, 30 * mm)
    rows = [
        ["Aspecto", "DEV", "PROD", "Beneficio"],
        ["Base de datos", "localhost y puerto fijo", "DB_HOST, DB_PORT y DB_NAME", "Despliegue portable"],
        ["SQL", "show-sql: true", "show-sql: false", "Diagnostico sin ruido productivo"],
        ["Health", "show-details: always", "show-details: never", "Menor exposicion de informacion"],
        ["Swagger", "Disponible", "Deshabilitado", "Superficie reducida en produccion"],
        ["Artefacto Java", "El mismo JAR", "El mismo JAR", "No requiere recompilacion"],
    ]
    table = Table(rows, colWidths=[40 * mm, 58 * mm, 69 * mm, 80 * mm], rowHeights=[9 * mm] + [12 * mm] * 5)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT), ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("GRID", (0, 0), (-1, -1), 0.5, MID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    table.wrapOn(c, PAGE_W - 36 * mm, 70 * mm); table.drawOn(c, 18 * mm, 69 * mm)
    c.setFillColor(colors.HexColor("#EAF6F0")); c.roundRect(18 * mm, 27 * mm, PAGE_W - 36 * mm, 30 * mm, 3 * mm, fill=1, stroke=0)
    para(c, "<b>Conclusion tecnica:</b> al promover una version no se modifican ni duplican fuentes. El ambiente selecciona su perfil y Config Server entrega valores versionados. Esto reduce configuracion divergente, permite auditoria en Git y facilita replicar instancias con el mismo contrato operativo.", BODY, 24 * mm, 51 * mm, PAGE_W - 48 * mm, 24 * mm)
    footer(c, 8); c.showPage()

    evidence_page(c, 9, "Evidencia 6", "Error diagnosticado: perfil inexistente", "06_error_perfil.png", "comparacion entre la consulta incorrecta qa y la consulta correcta dev.", "qa retorna cero fuentes porque no existe orden-ms-qa.yml; se debe usar dev o crear el archivo con el nombre exacto.")

    # 10. Reflexion y cierre
    draw_header(c, "Cierre", "Reflexion y conclusiones")
    para(c, "Reflexion personal", H1, 18 * mm, PAGE_H - 36 * mm, 100 * mm)
    reflections = [
        "1. Config Server establece un punto unico y versionable para administrar propiedades compartidas.",
        "2. Cuando aumentan los microservicios e instancias, evita repetir manualmente la misma configuracion.",
        "3. Los perfiles DEV y PROD permiten cambiar infraestructura sin alterar ni recompilar el codigo.",
        "4. Cada instancia puede iniciar con el mismo artefacto y recibir valores coherentes para su ambiente.",
        "5. La trazabilidad en Git ayuda a revisar cambios, identificar responsables y recuperar versiones anteriores.",
        "6. Las pruebas de health, endpoints y errores reducen el riesgo de desplegar configuraciones incompletas.",
        "7. En conjunto, la solucion disminuye el configuration drift y simplifica el escalamiento horizontal.",
    ]
    y = PAGE_H - 54 * mm
    for item in reflections:
        c.setFillColor(LIGHT); c.roundRect(20 * mm, y - 8 * mm, 165 * mm, 10 * mm, 2 * mm, fill=1, stroke=0)
        para(c, item, SMALL, 24 * mm, y, 157 * mm, 9 * mm); y -= 13 * mm
    c.setFillColor(NAVY); c.roundRect(198 * mm, 50 * mm, 77 * mm, 89 * mm, 4 * mm, fill=1, stroke=0)
    para(c, "Entregables verificados", ParagraphStyle("whitehead", parent=H2, textColor=WHITE), 207 * mm, 130 * mm, 60 * mm)
    checklist = ["Config Server UP", "orden-ms DEV/PROD", "Config Client activo", "Health y CRUD", "Catalogo DEV/PROD", "Error documentado"]
    yy = 112 * mm
    for item in checklist:
        c.setFillColor(GREEN); c.circle(210 * mm, yy + 1 * mm, 2.2 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8); c.drawCentredString(210 * mm, yy - 1 * mm, "OK")
        c.setFont("Helvetica", 9); c.drawString(216 * mm, yy - 1 * mm, item); yy -= 11 * mm
    para(c, "<b>Repositorio:</b><br/>https://github.com/Aldo-Ct/Pagalotu<br/><br/><b>Referencia de la actividad:</b><br/>262dist.github.io/pagatu/sesiones/S02_Configuracion_Centralizada_Ambientes/", SMALL, 198 * mm, 41 * mm, 78 * mm, 30 * mm)
    footer(c, 10); c.showPage()

    c.save()
    print(OUT)


if __name__ == "__main__":
    make_pdf()
