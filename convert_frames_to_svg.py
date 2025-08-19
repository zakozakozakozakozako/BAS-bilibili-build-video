#!/usr/bin/env python3
import os
import zipfile
from PIL import Image
import numpy as np
import potrace

def curve_to_svg(curve):
    """
    将 potrace.Curve 转为 SVG path d 字符串
    """
    d = []
    start = curve.start_point
    d.append(f'M {start[0]} {start[1]}')
    for segment in curve:
        if segment.is_corner:
            c = segment.c
            d.append(f'L {c[0]} {c[1]}')
        else:  # bezier segment
            c1, c2, end = segment.c1, segment.c2, segment.end_point
            d.append(f'C {c1[0]} {c1[1]} {c2[0]} {c2[1]} {end[0]} {end[1]}')
    return ' '.join(d)

os.makedirs("segmented", exist_ok=True)

frames_dir = "frames"
frames = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])

threshold = 128

for fname in frames:
    src = os.path.join(frames_dir, fname)
    img = Image.open(src).convert("L")
    arr = np.array(img)
    bitmap = (arr > threshold).astype(np.uint8)
    bmp = potrace.Bitmap(bitmap)
    path_obj = bmp.trace()
    svg_path = os.path.join("segmented", os.path.splitext(fname)[0]+".svg")
    h, w = arr.shape

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n')
        for curve in path_obj:
            d_str = curve_to_svg(curve)
            f.write(f'  <path d="{d_str}" fill="black" stroke="none"/>\n')
        f.write('</svg>\n')

# 打包 segmented 文件夹
zip_name = "guanjia.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("segmented"):
        for f_name in sorted(files):
            full = os.path.join(root, f_name)
            arcname = os.path.relpath(full, start="segmented")
            z.write(full, arcname=arcname)

print("Created", zip_name)