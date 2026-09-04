from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
ART = PROJECT / "03_ilustraciones" / "portada"

BACK_BACKGROUND = ART / "contraportada-fondo-v1.png"
FRONT = ART / "portada_12_armaduras-historicas-v2-titulo.png"
BACK_OUTPUT = ART / "contraportada-v2-texto-aprobado.png"
SPREAD_OUTPUT = ART / "cubierta-doble-v2-texto-aprobado.png"

GOTHIC_FONT = ROOT / "tmp" / "fonts" / "CinzelDecorative-Black.ttf"
BODY_FONT = Path("C:/Windows/Fonts/georgia.ttf")
BODY_ITALIC_FONT = Path("C:/Windows/Fonts/georgiai.ttf")

GOLD = "#f2cb69"
LIGHT_GOLD = "#ffe3a3"
SOFT_GOLD = "#e4c178"
SHADOW = "#07182c"


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    stroke_width: int = 0,
) -> None:
    draw.text(
        xy,
        text,
        font=font,
        fill=fill,
        anchor="mm",
        align="center",
        stroke_width=stroke_width,
        stroke_fill=SHADOW,
    )


def build_back(size: int) -> Image.Image:
    back = Image.open(BACK_BACKGROUND).convert("RGB")
    if back.size != (size, size):
        back = back.resize((size, size), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(back)
    heading = ImageFont.truetype(GOTHIC_FONT, round(size * 0.047))
    heading_small = ImageFont.truetype(GOTHIC_FONT, round(size * 0.034))
    body = ImageFont.truetype(BODY_FONT, round(size * 0.021))
    closing = ImageFont.truetype(GOTHIC_FONT, round(size * 0.019))

    cx = round(size * 0.50)
    centered_text(draw, (cx, round(size * 0.155)), "DOCE ARMADURAS", heading, GOLD, 2)
    centered_text(draw, (cx, round(size * 0.210)), "DOCE HISTORIAS", heading, GOLD, 2)
    centered_text(draw, (cx, round(size * 0.263)), "UNA NIÑA DISPUESTA A", heading_small, GOLD, 2)
    centered_text(draw, (cx, round(size * 0.307)), "DESCUBRIR SU VALOR", heading_small, GOLD, 2)

    line_y = round(size * 0.350)
    draw.line(
        (round(size * 0.31), line_y, round(size * 0.47), line_y),
        fill=GOLD,
        width=max(2, round(size * 0.002)),
    )
    draw.ellipse(
        (
            cx - round(size * 0.009),
            line_y - round(size * 0.009),
            cx + round(size * 0.009),
            line_y + round(size * 0.009),
        ),
        outline=GOLD,
        width=max(2, round(size * 0.002)),
    )
    draw.line(
        (round(size * 0.53), line_y, round(size * 0.69), line_y),
        fill=GOLD,
        width=max(2, round(size * 0.002)),
    )

    lines = [
        "En una sala llena de estrellas,",
        "doce armaduras esperan a Ana-Sophia.",
        "",
        "Cada una guarda la historia de una mujer",
        "que dejó su huella en el mundo:",
        "reinas, arqueras, estrategas y defensoras",
        "que se atrevieron a actuar cuando parecía",
        "que nadie más podía hacerlo.",
        "",
        "Al ponerse cada armadura, Ana-Sophia viajará",
        "a otra época y descubrirá que ser valiente",
        "no significa no tener miedo.",
        "Significa pensar, levantarse, proteger",
        "a los demás y seguir adelante.",
    ]
    y = round(size * 0.390)
    step = round(size * 0.030)
    for line in lines:
        if line:
            centered_text(draw, (cx, y), line, body, LIGHT_GOLD, 2)
        y += step

    centered_text(
        draw,
        (cx, round(size * 0.865)),
        "DOCE VIAJES POR LA HISTORIA",
        closing,
        GOLD,
        2,
    )
    centered_text(
        draw,
        (cx, round(size * 0.904)),
        "DOCE MANERAS DE SER VALIENTE",
        closing,
        GOLD,
        2,
    )
    centered_text(
        draw,
        (cx, round(size * 0.950)),
        "Una aventura creada especialmente para Ana-Sophia",
        ImageFont.truetype(BODY_ITALIC_FONT, round(size * 0.021)),
        SOFT_GOLD,
        2,
    )
    return back


def main() -> None:
    front = Image.open(FRONT).convert("RGB")
    size = front.height
    if front.width != size:
        front = front.resize((size, size), Image.Resampling.LANCZOS)

    back = build_back(size)
    back.save(BACK_OUTPUT, quality=95)

    spread = Image.new("RGB", (size * 2, size))
    spread.paste(back, (0, 0))
    spread.paste(front, (size, 0))
    spread.save(SPREAD_OUTPUT, quality=95)

    print(BACK_OUTPUT)
    print(SPREAD_OUTPUT)


if __name__ == "__main__":
    main()
