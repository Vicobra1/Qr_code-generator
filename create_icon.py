"""Create the Kobra QR Windows icon using Pillow."""

from pathlib import Path

from PIL import Image, ImageDraw


SIZE = 256
BACKGROUND = "#10151e"
ACCENT = "#55d6c2"
INK = "#17302f"
OUTPUT = Path(__file__).with_name("kobra_qr.ico")


def draw_finder(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.rounded_rectangle((x, y, x + 61, y + 61), radius=11, fill=ACCENT)
    draw.rounded_rectangle((x + 12, y + 12, x + 49, y + 49), radius=7, fill=BACKGROUND)
    draw.rounded_rectangle((x + 23, y + 23, x + 38, y + 38), radius=4, fill=ACCENT)


def main() -> None:
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 248, 248), radius=48, fill=BACKGROUND)

    draw_finder(draw, 37, 37)
    draw_finder(draw, 158, 37)
    draw_finder(draw, 37, 158)

    modules = [
        (112, 44, 128, 60), (112, 70, 128, 86), (102, 98, 118, 114),
        (127, 100, 143, 116), (155, 104, 171, 120), (185, 108, 201, 124),
        (98, 127, 114, 143), (126, 133, 142, 149), (153, 133, 169, 149),
        (181, 137, 197, 153), (102, 159, 118, 175), (128, 164, 144, 180),
        (155, 165, 171, 181), (187, 165, 203, 181), (103, 190, 119, 206),
        (128, 194, 144, 210), (157, 194, 173, 210), (188, 195, 204, 211),
        (101, 218, 117, 234), (130, 218, 146, 234), (160, 218, 176, 234),
        (190, 218, 206, 234),
    ]
    for module in modules:
        draw.rounded_rectangle(module, radius=3, fill=ACCENT)

    # Small dark cut-outs give the lower-right modules a QR-like rhythm.
    for x, y in ((133, 168), (161, 141), (190, 113), (163, 222)):
        draw.rectangle((x, y, x + 6, y + 6), fill=INK)

    image.save(OUTPUT, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Icône créée : {OUTPUT}")


if __name__ == "__main__":
    main()
