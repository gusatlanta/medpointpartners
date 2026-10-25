"""Render the MedPoint shield mark to PNG favicons and the social share image.

The vector source is img/mp-mark.svg; this redraws the same shapes with Pillow
(no SVG renderer needed). Run from the site root:  python tools/make_images.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
SS = 8  # supersampling factor for smooth edges

NAVY_TOP = (36, 57, 122)
NAVY = (12, 26, 64)
BLUE = (47, 132, 220)
WHITE = (255, 255, 255)


def bezier(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def shield(top, right, side_y, ctrl, bottom):
    """Shield outline in the 64x74 mark space (same path as mp-mark.svg)."""
    l = 64 - right
    pts = [(32, top), (right, top + 8 * (right - 32) / 28 if right == 60 else 13.3), (right, side_y)]
    pts += bezier((right, side_y), (right, ctrl[0]), (32 + ctrl[1], ctrl[2]), (32, bottom))[1:]
    pts += bezier((32, bottom), (32 - ctrl[1], ctrl[2]), (l, ctrl[0]), (l, side_y))[1:]
    pts += [(l, pts[1][1])]
    return pts


OUTER = shield(2, 60, 34, (52, 16, 64), 72)
INNER = shield(6.5, 56, 34, (49.5, 13.8, 60), 67.3)
CROSS = [(25.5, 19), (38.5, 19), (38.5, 29.5), (49, 29.5), (49, 42.5), (38.5, 42.5), (38.5, 53),
         (25.5, 53), (25.5, 42.5), (15, 42.5), (15, 29.5), (25.5, 29.5)]


def stroke_square(d, pts, width, fill):
    """Outline an axis-aligned polygon with crisp square corners."""
    hw = width / 2
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        d.rectangle([min(x1, x2) - hw, min(y1, y2) - hw, max(x1, x2) + hw, max(y1, y2) + hw], fill=fill)


def draw_mark(size_h):
    """Return an RGBA image of the mark, size_h pixels tall."""
    s = size_h * SS / 74
    w, h = round(64 * s), round(74 * s)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # vertical gradient fill clipped to the shield
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(h - 1, 1)
        gd.line([(0, y), (w, y)], fill=tuple(round(NAVY_TOP[i] + (NAVY[i] - NAVY_TOP[i]) * t) for i in range(3)) + (255,))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(x * s, y * s) for x, y in OUTER], fill=255)
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    d.line(sc(INNER + INNER[:1]), fill=WHITE + (230,), width=max(1, round(1.6 * s)), joint="curve")
    d.polygon(sc(CROSS), fill=BLUE + (150,))
    stroke_square(d, sc(CROSS), 3 * s, WHITE)
    return img.resize((max(1, round(w / SS)), size_h), Image.LANCZOS)


def square_icon(px, pad=0.06, bg=None):
    canvas = Image.new("RGBA", (px, px), bg or (0, 0, 0, 0))
    mark = draw_mark(round(px * (1 - 2 * pad)))
    canvas.alpha_composite(mark, ((px - mark.width) // 2, (px - mark.height) // 2))
    return canvas


def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def share_image():
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=(round(10 + 13 * t), round(22 + 39 * t), round(54 + 73 * t), 255))
    mark = draw_mark(300)
    img.alpha_composite(mark, (110, (H - mark.height) // 2 - 10))
    serif = font(["C:/Windows/Fonts/georgiab.ttf", "georgiab.ttf", "DejaVuSerif-Bold.ttf"], 96)
    sans = font(["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeui.ttf", "DejaVuSans.ttf"], 30)
    small = font(["C:/Windows/Fonts/segoeui.ttf", "DejaVuSans.ttf"], 30)
    x = 430
    d.text((x, 190), "MEDPOINT", font=serif, fill=WHITE)
    d.text((x + 4, 300), "P  A  R  T  N  E  R  S", font=sans, fill=(143, 195, 255))
    d.line([(x, 362), (x + 640, 362)], fill=(143, 195, 255, 120), width=2)
    d.text((x, 386), "Healthcare Finance & Revenue Cycle Recruiting", font=small, fill=(225, 232, 245))
    d.text((x, 430), "Atlanta, GA  ·  Powered by NorthPoint", font=small, fill=(170, 185, 215))
    return img.convert("RGB")


if __name__ == "__main__":
    square_icon(32, pad=0.02).save(IMG / "favicon-32.png")
    square_icon(180, pad=0.1, bg=(255, 255, 255, 255)).save(IMG / "favicon-180.png")
    square_icon(512, pad=0.06).save(IMG / "favicon-512.png")
    share_image().save(IMG / "og-image.png", optimize=True)
    print("wrote", ", ".join(p.name for p in sorted(IMG.glob("*.png"))))
