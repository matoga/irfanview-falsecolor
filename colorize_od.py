import argparse, sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ==== CONFIG ====
IRFANVIEW_PATH = r"C:\Program Files\IrfanView\i_view64.exe"
OUTPUT_DIR = r"C:\temp\OD_Colorized"
PALETTE_STOPS = [
  (0.000, (255, 255, 255)),  # white
  (0.030, (0, 0, 255)),      # blue
  (0.120, (0, 128, 255)),    # light blue
  (0.180, (0, 255, 255)),    # cyan
  (0.280, (0, 255, 128)),    # turquoise
  (0.450, (192, 255, 0)),    # lime-yellow
  (0.53, (255, 255, 0)),    # yellow
  (0.61, (255, 200, 0)),    # yellow-orange
  (0.68, (255, 160, 0)),    # orange
  (0.72, (255, 120, 0)),    # deep orange
  (0.78, (255, 60, 0)),     # reddish-orange
  (0.85, (255, 0, 0)),     # red
  (1.000, (120, 0, 0)),      # dark red
]
# =================

def make_custom_lut(n=256):
    xs = np.array([p for p,_ in PALETTE_STOPS], dtype=np.float32)
    cols = np.array([c for _,c in PALETTE_STOPS], dtype=np.float32)
    t = np.linspace(0.0, 1.0, n, dtype=np.float32)
    lut = np.zeros((n,3), dtype=np.uint8)
    for i in range(3):
        lut[:, i] = np.clip(np.interp(t, xs, cols[:, i]), 0, 255).astype(np.uint8)
    return lut

def load_raw(path):
    img = Image.open(path)
    arr = np.array(img)
    if arr.ndim == 3:
        arr = arr[..., 0]
    return arr

def decode_od_from_img(arr):
    od = arr.astype(np.float32) / 256.0 - 8.0
    return np.clip(od, 0.0, 3.0)

def map_od_to_rgb(od, lut):
    x = od / 3.0
    idx = np.clip((x * (len(lut) - 1)).astype(np.int32), 0, len(lut)-1)
    return lut[idx]

def add_colorbar(img, lut, width=40, ticks=7):
    """Add a vertical colorbar with OD ticks to the right of the image."""
    h = img.height
    bar = Image.new("RGB", (width, h), (255, 255, 255))
    # Fill gradient
    for y in range(h):
        frac = 1.0 - y / (h - 1)  # top=OD=3, bottom=OD=0
        idx = int(frac * (len(lut) - 1))
        bar.paste(tuple(lut[idx]), (0, y, width, y+1))
    # Draw ticks
    draw = ImageDraw.Draw(bar)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    for i in range(ticks):
        od_val = 3.0 * (1 - i / (ticks - 1))
        y_pos = int(i * (h - 1) / (ticks - 1))
        draw.line([(0, y_pos), (width//3, y_pos)], fill=(0,0,0))
        draw.text((width//2, y_pos - 7), f"{od_val:.1f}", fill=(0,0,0), font=font)
    # Combine
    combined = Image.new("RGB", (img.width + width, h))
    combined.paste(img, (0, 0))
    combined.paste(bar, (img.width, 0))
    return combined

def main():
    ap = argparse.ArgumentParser(description="False-color OD colorizer (fixed mapping, no autoscale)")
    ap.add_argument("input", help="Input image path (TIFF/PNG)")
    ap.add_argument("--colorbar", action="store_true", help="Add vertical colorbar with OD ticks")
    args = ap.parse_args()

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        arr = load_raw(args.input)
        od = decode_od_from_img(arr)
        lut = make_custom_lut(256)
        rgb = map_od_to_rgb(od, lut)
        img_out = Image.fromarray(rgb, mode="RGB")

        if args.colorbar:
            img_out = add_colorbar(img_out, lut)

        base_name = os.path.splitext(os.path.basename(args.input))[0]
        out_path = os.path.abspath(os.path.join(OUTPUT_DIR, base_name + ".odcolor.png"))
        img_out.save(out_path)

        # Launch in IrfanView
        if not os.path.exists(IRFANVIEW_PATH):
            raise FileNotFoundError(f"IrfanView not found at: {IRFANVIEW_PATH}")
        subprocess.Popen([IRFANVIEW_PATH, out_path])

    except Exception as e:
        print("❌ ERROR:", e)
        input("Press Enter to close...")

if __name__ == "__main__":
    sys.exit(main())