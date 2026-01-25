from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np

root = Path(r"C:\Users\kevin\New folder (2)")

source = root / "Gemini_Generated_Image_60zpje60zpje60zp.png"
if not source.exists():
    matches = sorted(root.glob("Gemini_Generated_Image_*.png"))
    if not matches:
        raise SystemExit(f"Source not found: {source}")
    source = matches[-1]

out_dir = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets")
out_dir.mkdir(parents=True, exist_ok=True)

orig = Image.open(source).convert("RGBA")

# Cutout with alpha only, no color adjustments
cutout = remove(orig)
cutout_path = out_dir / "unit_cutout_clean.png"
cutout.save(cutout_path)

# Background with transparent hole (no inpainting, original colors preserved)
cutout_np = np.array(cutout)
alpha = cutout_np[:, :, 3]

orig_np = np.array(orig)
background_np = orig_np.copy()
background_np[alpha > 0, 3] = 0
background = Image.fromarray(background_np, mode="RGBA")
background_path = out_dir / "unit_background_clean.png"
background.save(background_path)

print(f"Saved clean cutout: {cutout_path}")
print(f"Saved clean background: {background_path}")
print(f"Source used: {source}")
