#!/usr/bin/env python3
"""Generates the bloated SVG files and HTML print pages for test_website2.

Run once from inside the test_website2 directory:
    python3 generate_bloat.py

Idempotent — re-running overwrites the generated files.
"""
import os
import random

random.seed(42)  # deterministic

HERE = os.path.dirname(os.path.abspath(__file__))
PRINTS = os.path.join(HERE, "prints")
os.makedirs(PRINTS, exist_ok=True)

COLORS = ["#FF8A3D", "#F26430", "#FFC79A", "#FFE6CC", "#FFD4B0", "#5A3A26", "#3A2516", "#6B4A33"]


def grid_svg(side_px, cell_count_per_side, radius_frac=0.4):
    """Returns an inline-SVG string: a grid of randomly colored circles."""
    cell = side_px / cell_count_per_side
    r = cell * radius_frac
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side_px} {side_px}" width="{side_px}" height="{side_px}">']
    parts.append(f'<rect width="{side_px}" height="{side_px}" fill="#FFF4E6"/>')
    for i in range(cell_count_per_side):
        for j in range(cell_count_per_side):
            cx = cell * (i + 0.5)
            cy = cell * (j + 0.5)
            color = COLORS[(i * 7 + j * 13) % len(COLORS)]
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}"/>')
    parts.append("</svg>")
    return "".join(parts)


# Standalone SVG files
with open(os.path.join(HERE, "small.svg"), "w") as f:
    # ~ a few KB: 10x10 grid = 100 circles
    f.write(grid_svg(400, 10))

with open(os.path.join(HERE, "medium.svg"), "w") as f:
    # ~ 50 KB: 60x60 grid = 3600 circles
    f.write(grid_svg(600, 60))

with open(os.path.join(HERE, "large.svg"), "w") as f:
    # ~ 500 KB: 200x200 grid = 40000 circles
    f.write(grid_svg(2000, 200))


def html_page(title, body):
    nav = '<nav><a href="/">Home</a> · <a href="/gallery.html">Gallery</a></nav>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Page Bloat Test Site</title>
</head>
<body>
<header>{nav}</header>
<main>
<h1>{title}</h1>
{body}
</main>
</body>
</html>
"""


# Small prints: pure text, ~ a few hundred bytes of body. Each references small.svg.
for n in range(1, 5):
    body = (
        f'<p>Print {n}. A small, lightweight catalog entry.</p>'
        f'<img src="/small.svg" alt="Print {n} thumbnail" width="200" height="200">'
    )
    with open(os.path.join(PRINTS, f"print-{n}.html"), "w") as f:
        f.write(html_page(f"Print {n}", body))

# Medium prints: reference medium.svg, plus a small inline SVG and some text.
for n in range(5, 9):
    inline = grid_svg(300, 20)  # ~ 5 KB inline
    body = (
        f'<p>Print {n}. Medium-weight page with both inline and referenced SVG.</p>'
        f'<div>{inline}</div>'
        f'<img src="/medium.svg" alt="Print {n} reference" width="400" height="400">'
    )
    with open(os.path.join(PRINTS, f"print-{n}.html"), "w") as f:
        f.write(html_page(f"Print {n}", body))

# Heavy prints: large inline SVG, no referenced images. ~ 80 KB each.
for n in range(9, 12):
    inline = grid_svg(800, 80)  # ~ 80 KB
    body = (
        f'<p>Print {n}. Heavy page — a large inline SVG drives the page weight up significantly.</p>'
        f'<div>{inline}</div>'
    )
    with open(os.path.join(PRINTS, f"print-{n}.html"), "w") as f:
        f.write(html_page(f"Print {n}", body))

# Bloated print: inline SVG + reference to large.svg + paragraphs of text.
inline = grid_svg(1000, 100)  # ~ 130 KB inline
paragraphs = "\n".join(
    "<p>" + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20).strip() + "</p>"
    for _ in range(60)
)  # ~ 60 KB text
body = (
    '<p>Print 12. The bloated showpiece: very large inline SVG, a separate large.svg reference, and many paragraphs of text.</p>'
    f'<div>{inline}</div>'
    f'<img src="/large.svg" alt="Print 12 reference" width="800" height="800">'
    f'<section>{paragraphs}</section>'
)
with open(os.path.join(PRINTS, "print-12.html"), "w") as f:
    f.write(html_page("Print 12", body))

# Report sizes for sanity
for name in ["small.svg", "medium.svg", "large.svg"]:
    path = os.path.join(HERE, name)
    print(f"  {name}: {os.path.getsize(path):,} bytes")
for n in range(1, 13):
    path = os.path.join(PRINTS, f"print-{n}.html")
    print(f"  prints/print-{n}.html: {os.path.getsize(path):,} bytes")
