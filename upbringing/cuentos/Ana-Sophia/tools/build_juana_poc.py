from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "upbringing" / "cuentos" / "Ana-Sophia"
IMAGES = PROJECT / "03_ilustraciones" / "01_juana_de_arco"
OUTPUT = ROOT / "output" / "pdf" / "doce_armaduras_ana_sophia_juana_poc.pdf"

PAGE = 210 * mm
PAPER = HexColor("#FFF8E8")
INK = HexColor("#26333A")
ACCENT = HexColor("#8B3E35")


def register_fonts():
    regular = Path("C:/Windows/Fonts/trebuc.ttf")
    bold = Path("C:/Windows/Fonts/trebucbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("BookSans", str(regular)))
        pdfmetrics.registerFont(TTFont("BookSansBold", str(bold)))
        return "BookSans", "BookSansBold"
    return "Helvetica", "Helvetica-Bold"


BODY_FONT, BOLD_FONT = register_fonts()


def draw_cover_image(c, path, x, y, width, height, focus_x=0.5, focus_y=0.5):
    image = ImageReader(str(path))
    image_width, image_height = image.getSize()
    scale = max(width / image_width, height / image_height)
    drawn_width = image_width * scale
    drawn_height = image_height * scale
    offset_x = x - (drawn_width - width) * focus_x
    offset_y = y - (drawn_height - height) * focus_y

    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        image,
        offset_x,
        offset_y,
        width=drawn_width,
        height=drawn_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    c.restoreState()


def wrapped_lines(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(c, text, x, top_y, width, font_size, leading, color=INK):
    lines = wrapped_lines(text, BODY_FONT, font_size, width)
    c.setFillColor(color)
    c.setFont(BODY_FONT, font_size)
    y = top_y
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def image_veil(c, x, y, width, height, alpha=0.12):
    c.saveState()
    c.setFillColor(PAPER)
    c.setFillAlpha(alpha)
    c.rect(x, y, width, height, stroke=0, fill=1)
    c.restoreState()


def translucent_box(c, x, y, width, height, alpha=0.88, radius=5 * mm):
    c.saveState()
    c.setFillColor(PAPER)
    c.setFillAlpha(alpha)
    c.roundRect(x, y, width, height, radius, stroke=0, fill=1)
    c.restoreState()


def page_one(c):
    image = IMAGES / "01_presentacion-ghibli-v2.png"
    draw_cover_image(c, image, 0, 0, PAGE, PAGE)
    image_veil(c, 0, 0, PAGE, PAGE, 0.10)

    title_x = 12 * mm
    title_y = PAGE - 49 * mm
    translucent_box(c, 8 * mm, title_y - 3 * mm, 108 * mm, 39 * mm, 0.86)
    c.setFillColor(ACCENT)
    c.setFont(BOLD_FONT, 11)
    c.drawString(title_x, PAGE - 22 * mm, "HOY ANA-SOPHIA ES...")
    c.setFillColor(INK)
    c.setFont(BOLD_FONT, 25)
    c.drawString(title_x, PAGE - 37 * mm, "JUANA DE ARCO")

    intro = (
        "En 1429, Francia e Inglaterra llevaban muchos años en guerra. La ciudad "
        "francesa de Orleans estaba rodeada por el ejército inglés y sus habitantes "
        "comenzaban a perder la esperanza. Si la ciudad caía, los ingleses podrían "
        "seguir avanzando. Entonces apareció Juana de Arco. Tenía unos diecisiete "
        "años, no pertenecía al ejército y nunca había dirigido una batalla, pero "
        "estaba convencida de que debía ayudar. Logró que el futuro rey de Francia "
        "confiara en ella, se puso una armadura y partió hacia Orleans con soldados "
        "y provisiones."
    )
    box_x = 8 * mm
    box_y = 7 * mm
    box_width = 194 * mm
    box_height = 63 * mm
    translucent_box(c, box_x, box_y, box_width, box_height, 0.90)
    draw_paragraph(
        c,
        intro,
        box_x + 8 * mm,
        box_y + box_height - 9 * mm,
        box_width - 16 * mm,
        12.2,
        15.2,
    )
    c.showPage()


def event_band(c, y, number, heading, paragraph, armour=None):
    band_x = 5 * mm
    band_y = y + 4 * mm
    band_width = PAGE - 10 * mm
    band_height = (48 if armour else 42) * mm
    translucent_box(c, band_x, band_y, band_width, band_height, 0.90, 4 * mm)

    circle_x = 14 * mm
    circle_y = band_y + band_height - 12 * mm
    c.setFillColor(ACCENT)
    c.circle(circle_x, circle_y, 6 * mm, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(BOLD_FONT, 14)
    c.drawCentredString(circle_x, circle_y - 1.7 * mm, str(number))

    text_x = 22 * mm
    c.setFillColor(ACCENT)
    c.setFont(BOLD_FONT, 13)
    c.drawString(text_x, band_y + band_height - 9 * mm, heading)
    body_bottom = draw_paragraph(
        c,
        paragraph,
        text_x,
        band_y + band_height - 17 * mm,
        PAGE - text_x - 10 * mm,
        10.5,
        12.8,
    )
    if armour:
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.8)
        c.line(text_x, band_y + 8 * mm, PAGE - 10 * mm, band_y + 8 * mm)
        c.setFillColor(ACCENT)
        c.setFont(BOLD_FONT, 10.5)
        c.drawString(text_x, band_y + 3.5 * mm, armour)
    if body_bottom < band_y + (11 * mm if armour else 4 * mm):
        raise RuntimeError(f"Text overflow in event {number}")


def page_two(c):
    half = PAGE / 2
    image_two = IMAGES / "02_anima_orleans-ghibli-v2.png"
    image_three = IMAGES / "03_rompe_cerco-ghibli-v2.png"
    draw_cover_image(c, image_two, 0, half, PAGE, half, focus_x=0.5, focus_y=0.5)
    draw_cover_image(c, image_three, 0, 0, PAGE, half, focus_x=0.5, focus_y=0.5)
    image_veil(c, 0, half, PAGE, half, 0.10)
    image_veil(c, 0, 0, PAGE, half, 0.10)

    event_one = (
        "Juana consiguió entrar en Orleans mientras el cerco aún continuaba. "
        "Recorrió las defensas, habló con los soldados y participó en los ataques "
        "contra las posiciones inglesas. Durante uno de ellos, una flecha la hirió, "
        "pero regresó junto a los combatientes. Su determinación hizo que un ejército "
        "cansado volviera a creer que la ciudad podía salvarse."
    )
    event_two = (
        "El 8 de mayo de 1429, los ingleses levantaron el sitio y se alejaron de "
        "Orleans. La guerra no había terminado, pero aquella victoria cambió su rumbo. "
        "Poco después, Juana acompañó al futuro Carlos VII hasta Reims, donde fue "
        "coronado rey. Al año siguiente fue capturada y, con solo diecinueve años, "
        "condenada en un juicio injusto. Años después, su nombre quedó rehabilitado."
    )

    event_band(c, half, 1, "ENTRÓ EN LA CIUDAD", event_one)
    event_band(
        c,
        0,
        2,
        "ROMPIÓ EL CERCO",
        event_two,
        "SU ARMADURA FUE LA ESPERANZA.",
    )
    c.showPage()


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=(PAGE, PAGE), pageCompression=1)
    pdf.setTitle("Doce armaduras para Ana-Sophia - PoC Juana de Arco")
    pdf.setAuthor("Proyecto familiar de Ana-Sophia")
    page_one(pdf)
    page_two(pdf)
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
