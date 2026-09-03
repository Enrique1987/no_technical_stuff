from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "upbringing" / "cuentos" / "Ana-Sophia"
IMAGE = PROJECT / "03_ilustraciones" / "01_juana_de_arco" / "01_presentacion-ghibli-v2.png"
OUTPUT = ROOT / "output" / "pdf" / "doce_armaduras_juana_pagina1_aprobada.pdf"
PAGE = 210 * mm

INK = HexColor("#2D2925")
BURGUNDY = HexColor("#78352F")
NAVY = HexColor("#18334A")
HALO = HexColor("#FFF3D1")
GOLD = HexColor("#B7852C")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Title", "C:/Windows/Fonts/Gabriola.ttf"))
    pdfmetrics.registerFont(TTFont("BodyBold", "C:/Windows/Fonts/georgiab.ttf"))


def draw_background(c):
    image = ImageReader(str(IMAGE))
    image_width, image_height = image.getSize()
    scale = max(PAGE / image_width, PAGE / image_height)
    width = image_width * scale
    height = image_height * scale
    c.drawImage(
        image,
        -(width - PAGE) / 2,
        -(height - PAGE) / 2,
        width=width,
        height=height,
        preserveAspectRatio=True,
        mask="auto",
    )


def wrap(text, font_name, font_size, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_outlined_lines(
    c,
    lines,
    x,
    top_y,
    font_size,
    leading,
    fill,
    stroke,
    stroke_width,
):
    c.saveState()
    c.setLineWidth(stroke_width)
    text = c.beginText(x, top_y)
    text.setFont("BodyBold", font_size)
    text.setLeading(leading)
    text.setFillColor(fill)
    text.setStrokeColor(stroke)
    text.setTextRenderMode(2)
    for line in lines:
        text.textLine(line)
    c.drawText(text)
    c.restoreState()


def draw_title(c):
    x = 11 * mm
    c.setLineWidth(0.22)
    subtitle = c.beginText(x, PAGE - 16 * mm)
    subtitle.setFont("BodyBold", 10)
    subtitle.setFillColor(BURGUNDY)
    subtitle.setStrokeColor(HALO)
    subtitle.setTextRenderMode(2)
    subtitle.textOut("HOY ANA-SOPHIA ES...")
    c.drawText(subtitle)

    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(x, PAGE - 19 * mm, x + 42 * mm, PAGE - 19 * mm)

    c.setFont("Title", 39)
    c.setFillColor(HALO)
    c.drawString(x + 0.5 * mm, PAGE - 37.5 * mm, "Juana de Arco")
    c.setFillColor(BURGUNDY)
    c.drawString(x, PAGE - 37 * mm, "Juana de Arco")


def draw_story(c):
    texts = [
        (
            "En 1429, Francia e Inglaterra llevaban muchos años en guerra. "
            "La ciudad francesa de Orleans estaba rodeada por el ejército inglés "
            "y sus habitantes comenzaban a perder la esperanza. Si Orleans caía, "
            "los ingleses podrían seguir avanzando y Carlos, heredero al trono "
            "francés, perdería una ciudad fundamental."
        ),
        (
            "Entonces apareció Juana de Arco. Tenía unos diecisiete años y no era "
            "soldado ni pertenecía a una familia poderosa. Estaba convencida de que "
            "Dios le había confiado una misión: ayudar a Francia y llevar a Carlos "
            "hasta su coronación. Para llegar hasta él pidió ayuda al capitán Robert "
            "de Baudricourt. Al principio no la creyó, pero Juana regresó y siguió "
            "insistiendo hasta conseguir una pequeña escolta."
        ),
        (
            "Juana cabalgó durante once días por territorio peligroso hasta el "
            "castillo de Chinon. Allí habló con Carlos, que todavía no había sido "
            "coronado rey. Él y sus consejeros la escucharon, le hicieron muchas "
            "preguntas y ordenaron que fuera examinada. Finalmente decidieron confiar "
            "en ella: le prepararon una armadura, un estandarte y permiso para viajar "
            "hacia Orleans con soldados y provisiones."
        ),
    ]

    font_size = 9.2
    leading = 12.4
    x = 11 * mm
    width = 83 * mm
    top_positions = (PAGE - 57 * mm, PAGE - 98 * mm, PAGE - 151 * mm)
    colours = (
        (NAVY, HALO, 0.12),
        (HALO, BURGUNDY, 0.16),
        (HALO, BURGUNDY, 0.16),
    )

    for paragraph, top_y, (fill, stroke, stroke_width) in zip(
        texts, top_positions, colours
    ):
        lines = wrap(paragraph, "BodyBold", font_size, width)
        draw_outlined_lines(
            c,
            lines,
            x,
            top_y,
            font_size,
            leading,
            fill,
            stroke,
            stroke_width,
        )

    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    for divider_y in (PAGE - 91 * mm, PAGE - 144 * mm):
        c.line(x, divider_y, x + 31 * mm, divider_y)
        c.circle(x + 34 * mm, divider_y, 1.3 * mm, stroke=1, fill=0)
        c.line(x + 37 * mm, divider_y, x + 68 * mm, divider_y)
    c.restoreState()


def main():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=(PAGE, PAGE), pageCompression=1)
    pdf.setTitle("Doce armaduras para Ana-Sophia - Juana de Arco, página 1")
    pdf.setAuthor("Proyecto familiar de Ana-Sophia")
    draw_background(pdf)
    draw_title(pdf)
    draw_story(pdf)
    pdf.showPage()
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
