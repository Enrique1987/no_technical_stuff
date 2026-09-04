from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
OUTPUT = (
    PROJECT
    / "03_ilustraciones"
    / "00_preliminares"
    / "00_dedicatoria-v1.png"
)

SIZE = 1254
GOTHIC_FONT = ROOT / "tmp" / "fonts" / "CinzelDecorative-Black.ttf"
ITALIC_FONT = Path("C:/Windows/Fonts/georgiai.ttf")

PAPER = "#fffdf7"
GOLD = "#b8892e"
SOFT_GOLD = "#d8b96b"


def centered(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    draw.text((SIZE // 2, y), text, font=font, fill=fill, anchor="mm")


def main() -> None:
    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)

    title_font = ImageFont.truetype(GOTHIC_FONT, 57)
    body_font = ImageFont.truetype(ITALIC_FONT, 36)

    inset = 62
    draw.rounded_rectangle(
        (inset, inset, SIZE - inset, SIZE - inset),
        radius=7,
        outline=SOFT_GOLD,
        width=2,
    )

    cx = SIZE // 2
    star_y = 435
    radius = 13
    points = [
        (cx, star_y - radius),
        (cx + 4, star_y - 4),
        (cx + radius, star_y),
        (cx + 4, star_y + 4),
        (cx, star_y + radius),
        (cx - 4, star_y + 4),
        (cx - radius, star_y),
        (cx - 4, star_y - 4),
    ]
    draw.polygon(points, fill=GOLD)

    centered(draw, 515, "Para Ana-Sophia,", title_font, GOLD)

    divider_y = 570
    draw.line((cx - 115, divider_y, cx - 18, divider_y), fill=SOFT_GOLD, width=2)
    draw.ellipse((cx - 5, divider_y - 5, cx + 5, divider_y + 5), outline=GOLD, width=2)
    draw.line((cx + 18, divider_y, cx + 115, divider_y), fill=SOFT_GOLD, width=2)

    centered(draw, 650, "de tu papá y mamá,", body_font, GOLD)
    centered(draw, 704, "que te adoran.", body_font, GOLD)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page.save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
