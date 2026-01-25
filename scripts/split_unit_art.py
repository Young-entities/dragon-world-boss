from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np
import cv2

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
cutout = remove(orig)
cutout_path = out_dir / "unit_cutout.png"
cutout.save(cutout_path)

cutout_np = np.array(cutout)
alpha = cutout_np[:, :, 3]
mask = (alpha > 0).astype(np.uint8) * 255

orig_bgr = cv2.cvtColor(np.array(orig), cv2.COLOR_RGBA2BGR)
kernel = np.ones((5, 5), np.uint8)
mask_dilated = cv2.dilate(mask, kernel, iterations=2)

inpainted = cv2.inpaint(orig_bgr, mask_dilated, 3, cv2.INPAINT_TELEA)
background_path = out_dir / "unit_background.png"
cv2.imwrite(str(background_path), inpainted)

print(f"Saved cutout: {cutout_path}")
print(f"Saved background: {background_path}")
