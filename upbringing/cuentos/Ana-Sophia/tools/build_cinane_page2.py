"""Compose approved prose over two independent illustrations; never alter source art."""
import re
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader

PROJECT = Path(__file__).resolve().parents[1]
ART = PROJECT / '03_ilustraciones' / '02_cinane'
OUTPUT = PROJECT / '05_impresion' / 'pruebas' / 'cinane-pagina-2-con-texto.pdf'
PAGE = 210 * mm
HALF = PAGE / 2
FONT_SIZE = 8.9
LEADING = 11.35
WIDTH = 94 * mm
INK = HexColor('#172C3A')


def paragraphs():
    source = (PROJECT / '01_textos' / '02_cinane.md').read_text(encoding='utf-8')
    section = source.split('## Página derecha', 1)[1].split('## La armadura', 1)[0]
    items = re.findall(r'(?ms)^### Texto[^\n]*\n\n(.*?)(?=\n### Texto|\Z)', section)
    result = [re.sub(r'\s+', ' ', item).strip() for item in items]
    assert len(result) == 3
    return result


def wrap(paragraph):
    lines, current = [], ''
    for word in paragraph.split():
        candidate = f'{current} {word}'.strip()
        if pdfmetrics.stringWidth(candidate, 'Body', FONT_SIZE) > WIDTH and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_text(pdf, paragraph, baseline):
    lines = wrap(paragraph)
    obj = pdf.beginText(8 * mm, baseline)
    obj.setFont('Body', FONT_SIZE)
    obj.setLeading(LEADING)
    obj.setFillColor(INK)
    obj.setTextRenderMode(0)
    for line in lines:
        obj.textLine(line)
    pdf.drawText(obj)
    return baseline - (len(lines) - 1) * LEADING


def main():
    pdfmetrics.registerFont(TTFont('Body', 'C:/Windows/Fonts/georgiab.ttf'))
    story = paragraphs()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=(PAGE, PAGE), pageCompression=1)
    pdf.setTitle('Cinane - segunda página con texto')
    pdf.setAuthor('Proyecto familiar de Ana-Sophia')
    pdf.drawImage(str(ART / '02_cruce_estrimon-ghibli-v3-texto.png'), 0, HALF, PAGE, HALF)
    pdf.drawImage(str(ART / '03_voluntad_cumplida-ghibli-v3.png'), 0, 0, PAGE, HALF)
    baseline = PAGE - 9 * mm
    end = draw_text(pdf, story[0], baseline)
    baseline2 = end - 8 * mm
    end2 = draw_text(pdf, story[1], baseline2)
    assert end2 > HALF + 5 * mm, 'Upper text exceeds panel'
    end3 = draw_text(pdf, story[2], HALF - 10 * mm)
    assert end3 > 45 * mm, 'Lower text enters dark foreground'
    pdf.showPage()
    pdf.save()
    extracted = re.sub(r'\s+', ' ', PdfReader(OUTPUT).pages[0].extract_text()).strip()
    assert extracted == ' '.join(story), 'Exported prose differs from approved source'
    print(f'Saved {OUTPUT}')
    print(f'Last baselines (mm): {end2/mm:.1f}, {end3/mm:.1f}')


if __name__ == '__main__':
    main()
