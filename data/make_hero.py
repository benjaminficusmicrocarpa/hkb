#!/usr/bin/env python3
"""Crop a species photo into a wide hero WebP.

The page banner is a short full-width strip. A portrait plate resized on its
long side, then cover-cropped by the browser, is only about a thousand pixels
wide and gets stretched. Crop the original to the banner first, then resize.

Output: ~heroes/{blp}.webp
Cloudflare id, when uploaded: hkb-{blp}-hero
The carousel plate is left whole. This file is not a plate.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

HKB = Path(__file__).resolve().parents[1]
ORIGINALS = HKB / "~original-jpg"
HEROES = HKB / "~heroes"
# Banner is wider than 16:9 and shorter than a 3:2 plate. 12:5 keeps the
# subject in a desktop header without a square mobile crop throwing it away.
ASPECT = 12 / 5
SHORT_SIDE = 720
WEBP_QUALITY = 80


def crop_hero(src: Path, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")
    width, height = img.size
    window_h = max(1, round(width / ASPECT))
    if window_h >= height:
        # Already wide enough. Crop the sides if needed, never the subject band.
        window_h = height
        window_w = min(width, round(height * ASPECT))
        left = (width - window_w) // 2
        box = (left, 0, left + window_w, height)
    else:
        top = _band_top(img, window_h)
        box = (0, top, width, top + window_h)
    cropped = img.crop(box)
    cw, ch = cropped.size
    short = min(cw, ch)
    if short > SHORT_SIDE:
        scale = SHORT_SIDE / short
        cropped = cropped.resize((round(cw * scale), round(ch * scale)), Image.Resampling.LANCZOS)
    cropped.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
    return cropped.size


def _band_top(img: Image.Image, window_h: int) -> int:
    """Place the horizontal window on the most colourful rows, not empty sky."""
    small = img.resize((80, max(1, round(80 * img.height / img.width))), Image.Resampling.BOX)
    sw, sh = small.size
    data = small.tobytes()
    row_score = []
    stride = sw * 3
    for y in range(sh):
        row = data[y * stride:(y + 1) * stride]
        score = 0
        for i in range(0, len(row), 3):
            r, g, b = row[i], row[i + 1], row[i + 2]
            score += max(r, g, b) - min(r, g, b)
        row_score.append(score)
    scale = img.height / sh
    win = max(1, round(window_h / scale))
    if win >= sh:
        return 0
    best_y = 0
    best = -1
    running = sum(row_score[:win])
    for y in range(0, sh - win + 1):
        # Mild centre pull so a bright corner does not steal the banner.
        centre = 1 - abs((y + win / 2) - sh / 2) / (sh / 2)
        scored = running * (0.75 + 0.25 * centre)
        if scored > best:
            best = scored
            best_y = y
        if y + win < sh:
            running += row_score[y + win] - row_score[y]
    top = round(best_y * scale)
    return max(0, min(top, img.height - window_h))


if __name__ == "__main__":
    import sys

    blp, code = sys.argv[1], sys.argv[2]
    src = ORIGINALS / blp / f"{code}.jpg"
    if not src.exists():
        raise SystemExit(f"missing {src}")
    dest = HEROES / f"{blp}.webp"
    size = crop_hero(src, dest)
    print(f"{dest} {size[0]}x{size[1]}")
