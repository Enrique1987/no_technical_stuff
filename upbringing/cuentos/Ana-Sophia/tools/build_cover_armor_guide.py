from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = (
    PROJECT
    / "03_ilustraciones"
    / "portada"
    / "portada_12_armaduras-historicas-v2.png"
)
OUTPUT = (
    PROJECT
    / "03_ilustraciones"
    / "portada"
    / "portada_12_armaduras-historicas-v2-guia.png"
)

CANVAS_SIZE = (2150, 1510)
IMAGE_ORIGIN = (448, 155)
IMAGE_SIZE = 1254

NAVY = "#071b35"
PANEL = "#102b4d"
PANEL_BORDER = "#e5b957"
GOLD = "#f1ca6b"
IVORY = "#fff3d2"
MUTED = "#b9c8d8"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path("C:/Windows/Fonts") / name, size)


def target(x: int, y: int) -> tuple[int, int]:
    return IMAGE_ORIGIN[0] + x, IMAGE_ORIGIN[1] + y


ARMORS = [
    {
        "number": 12,
        "name": "Artemisia I of Caria",
        "detail": "Caria · 5th c. BCE",
        "side": "left",
        "box_y": 175,
        "target": target(385, 185),
    },
    {
        "number": 11,
        "name": "Trưng Trắc",
        "detail": "Lạc Việt · 1st c. CE",
        "side": "left",
        "box_y": 365,
        "target": target(170, 340),
    },
    {
        "number": 10,
        "name": "Joan of Arc",
        "detail": "France · 15th c.",
        "side": "left",
        "box_y": 555,
        "target": target(105, 600),
    },
    {
        "number": 9,
        "name": "Lady Six Monkey",
        "detail": "Mixtec · 11th c.",
        "side": "left",
        "box_y": 745,
        "target": target(155, 840),
    },
    {
        "number": 8,
        "name": "Tomyris",
        "detail": "Massagetae · 6th c. BCE",
        "side": "left",
        "box_y": 935,
        "target": target(330, 1015),
    },
    {
        "number": 7,
        "name": "Hangaku Gozen",
        "detail": "Japan · 1201 CE",
        "side": "left",
        "box_y": 1125,
        "target": target(625, 1120),
    },
    {
        "number": 1,
        "name": "Cynane",
        "detail": "Macedon · 4th c. BCE",
        "side": "right",
        "box_y": 175,
        "target": target(625, 145),
    },
    {
        "number": 2,
        "name": "Khutulun",
        "detail": "Mongol world · 13th c.",
        "side": "right",
        "box_y": 365,
        "target": target(865, 180),
    },
    {
        "number": 3,
        "name": "Mavia",
        "detail": "Tanukhids · 4th c. CE",
        "side": "right",
        "box_y": 555,
        "target": target(1060, 340),
    },
    {
        "number": 4,
        "name": "Amanirenas",
        "detail": "Kush · 1st c. BCE",
        "side": "right",
        "box_y": 745,
        "target": target(1125, 590),
    },
    {
        "number": 5,
        "name": "Sichelgaita of Salerno",
        "detail": "Southern Italy · 11th c.",
        "side": "right",
        "box_y": 935,
        "target": target(1065, 830),
    },
    {
        "number": 6,
        "name": "Fu Hao",
        "detail": "Shang China · c. 1200 BCE",
        "side": "right",
        "box_y": 1125,
        "target": target(910, 1015),
    },
]


def draw_label(draw: ImageDraw.ImageDraw, item: dict, fonts: dict) -> None:
    box_w = 400
    box_h = 118
    x = 18 if item["side"] == "left" else CANVAS_SIZE[0] - 18 - box_w
    y = item["box_y"]
    box = (x, y, x + box_w, y + box_h)

    line_start = (
        (x + box_w, y + box_h // 2)
        if item["side"] == "left"
        else (x, y + box_h // 2)
    )
    elbow_x = IMAGE_ORIGIN[0] - 18 if item["side"] == "left" else IMAGE_ORIGIN[0] + IMAGE_SIZE + 18
    draw.line(
        [line_start, (elbow_x, line_start[1]), item["target"]],
        fill=GOLD,
        width=4,
        joint="curve",
    )
    tx, ty = item["target"]
    draw.ellipse((tx - 9, ty - 9, tx + 9, ty + 9), fill=GOLD, outline=NAVY, width=3)

    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=PANEL_BORDER, width=3)
    badge = (x + 14, y + 25, x + 76, y + 87)
    draw.ellipse(badge, fill=GOLD, outline=IVORY, width=2)
    number = str(item["number"])
    nb = draw.textbbox((0, 0), number, font=fonts["number"])
    draw.text(
        (
            (badge[0] + badge[2] - (nb[2] - nb[0])) / 2,
            (badge[1] + badge[3] - (nb[3] - nb[1])) / 2 - 3,
        ),
        number,
        font=fonts["number"],
        fill=NAVY,
    )
    draw.text((x + 88, y + 23), item["name"], font=fonts["name"], fill=IVORY)
    draw.text((x + 88, y + 69), item["detail"], font=fonts["detail"], fill=MUTED)


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    if source.size != (IMAGE_SIZE, IMAGE_SIZE):
        source = source.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", CANVAS_SIZE, NAVY)
    canvas.paste(source, IMAGE_ORIGIN)
    draw = ImageDraw.Draw(canvas)

    fonts = {
        "title": font("segoeuib.ttf", 46),
        "subtitle": font("segoeui.ttf", 24),
        "number": font("segoeuib.ttf", 28),
        "name": font("segoeuib.ttf", 27),
        "detail": font("segoeui.ttf", 20),
    }

    title = "ARMOR REFERENCE — WORKING MAP"
    title_box = draw.textbbox((0, 0), title, font=fonts["title"])
    draw.text(
        ((CANVAS_SIZE[0] - (title_box[2] - title_box[0])) / 2, 28),
        title,
        font=fonts["title"],
        fill=GOLD,
    )
    subtitle = "Clockwise from the top · exactly twelve historical warrior women"
    subtitle_box = draw.textbbox((0, 0), subtitle, font=fonts["subtitle"])
    draw.text(
        ((CANVAS_SIZE[0] - (subtitle_box[2] - subtitle_box[0])) / 2, 91),
        subtitle,
        font=fonts["subtitle"],
        fill=MUTED,
    )

    for armor in ARMORS:
        draw_label(draw, armor, fonts)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
