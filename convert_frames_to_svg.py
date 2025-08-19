# --- injected guard (safe in Python) ---
import os, pathlib, subprocess
from PIL import Image

WORK = os.getcwd()
out_dir = os.path.join(WORK, "guanjia", "converted_svgs")
os.makedirs(out_dir, exist_ok=True)
frames_dir = os.path.join(WORK, "frames")
# --- end injected guard ---

def convert_to_svg(frame_path, svg_path):
    # 临时 pbm 文件
    pbm_path = frame_path.replace(".png", ".pbm")
    # 转成黑白 pbm
    img = Image.open(frame_path).convert("1")
    img.save(pbm_path, "PPM")  # Pillow 会存成 PBM/PPM

    # 调用 potrace
    subprocess.run(["potrace", "-s", pbm_path, "-o", svg_path], check=True)

    # 可选：转完删除 pbm
    os.remove(pbm_path)

def main():
    for fname in sorted(os.listdir(frames_dir)):
        if fname.lower().endswith(".png"):
            frame_path = os.path.join(frames_dir, fname)
            svg_name = os.path.splitext(fname)[0] + ".svg"
            svg_path = os.path.join(out_dir, svg_name)
            print(f"Converting {frame_path} -> {svg_path}")
            convert_to_svg(frame_path, svg_path)

if __name__ == "__main__":
    main()