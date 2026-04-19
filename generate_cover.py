"""
Generate agent-handoff-skill cover image (2560x1280).
Deep plum / indigo gradient, bold monospace title, muted subtitle, rounded corners.
Composition intentionally mirrors the reference repo's public cover layout while using a distinct palette.
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 2560, 1280
CORNER_RADIUS = 80


def make_blob(size, color_rgba, cx, cy, rx, ry):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color_rgba)
    return layer


# ── 1. Base canvas (deep night plum) ─────────────────────────────────────────
base = Image.new("RGBA", (W, H), (14, 10, 24, 255))

# ── 2. Color blobs ────────────────────────────────────────────────────────────
blobs = [
    # (r, g, b, alpha,  cx,    cy,   rx,   ry,  blur)
    (76, 42, 138, 210, 720, 600, 760, 520, 120),
    (126, 87, 194, 160, 1940, 220, 620, 400, 100),
    (28, 17, 58, 185, 1320, 1140, 920, 360, 90),
    (43, 88, 188, 120, 1440, 640, 520, 360, 80),
    (236, 115, 87, 85, 320, 1030, 620, 420, 95),
]

canvas = base.copy()
for r, g, b, a, cx, cy, rx, ry, blur in blobs:
    blob = make_blob((W, H), (r, g, b, a), cx, cy, rx, ry)
    blob = blob.filter(ImageFilter.GaussianBlur(radius=blur))
    canvas = Image.alpha_composite(canvas, blob)

canvas = canvas.filter(ImageFilter.GaussianBlur(radius=8))

# ── 3. Film grain ────────────────────────────────────────────────────────────
rng = np.random.default_rng(24)
noise = rng.integers(0, 255, (H, W), dtype=np.uint8)
grain_alpha = (noise * 0.18).astype(np.uint8)
grain_layer = np.stack([noise, noise, noise, grain_alpha], axis=-1).astype(np.uint8)
grain_img = Image.fromarray(grain_layer, "RGBA")
canvas = Image.alpha_composite(canvas, grain_img)

# ── 4. Fonts (same usage pattern as reference) ───────────────────────────────
TITLE_SIZE = 220
SUBTITLE_SIZE = 68

try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", TITLE_SIZE, index=1)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", SUBTITLE_SIZE, index=0)
except Exception:
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", TITLE_SIZE)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", SUBTITLE_SIZE)

TITLE_TEXT = "agent-handoff-skill"
SUBTITLE_TEXT = "Continuation-ready HANDOFF.md for clean agent transfer."

# ── 5. Measure text ───────────────────────────────────────────────────────────
tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(tmp)

t_bbox = d.textbbox((0, 0), TITLE_TEXT, font=font_title)
t_w = t_bbox[2] - t_bbox[0]
t_h = t_bbox[3] - t_bbox[1]

s_bbox = d.textbbox((0, 0), SUBTITLE_TEXT, font=font_subtitle)
s_w = s_bbox[2] - s_bbox[0]
s_h = s_bbox[3] - s_bbox[1]

GAP = 48
total_h = t_h + GAP + s_h
block_top = (H - total_h) // 2 - 30

title_x = (W - t_w) // 2 - t_bbox[0]
title_y = block_top - t_bbox[1]

subtitle_x = (W - s_w) // 2 - s_bbox[0]
subtitle_y = title_y + t_h + GAP


def draw_text_layer(text, x, y, font, color):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((x, y), text, font=font, fill=color)
    return layer


# ── 6. Title with plum-blue glow ─────────────────────────────────────────────
glow_specs = [
    ((164, 132, 255, 62), 18),
    ((112, 180, 255, 92), 9),
    ((255, 169, 122, 110), 4),
]
for color, blur_r in glow_specs:
    glow = draw_text_layer(TITLE_TEXT, title_x, title_y, font_title, color)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_r))
    canvas = Image.alpha_composite(canvas, glow)

title_layer = draw_text_layer(TITLE_TEXT, title_x, title_y, font_title, (248, 245, 255, 245))
canvas = Image.alpha_composite(canvas, title_layer)

# ── 7. Subtitle ───────────────────────────────────────────────────────────────
subtitle_layer = draw_text_layer(
    SUBTITLE_TEXT, subtitle_x, subtitle_y, font_subtitle, (220, 210, 232, 214)
)
canvas = Image.alpha_composite(canvas, subtitle_layer)

# ── 8. Rounded corner mask ────────────────────────────────────────────────────
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (W - 1, H - 1)], radius=CORNER_RADIUS, fill=255)
canvas.putalpha(mask)

canvas = canvas.filter(ImageFilter.GaussianBlur(radius=1))

# ── 9. Save ───────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.png")
canvas.save(out_path, "PNG", dpi=(400, 400))
print(f"Saved: {out_path}")
print(f"Size: {canvas.size}")
