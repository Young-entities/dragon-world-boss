from pathlib import Path
from PIL import Image
import numpy as np

root = Path(r"C:\Users\kevin\New folder (2)")
assets = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets")
assets.mkdir(parents=True, exist_ok=True)

candidates = sorted(root.glob("Gemini_Generated_Image_*.png"))
if len(candidates) < 2:
    raise SystemExit("Need two Gemini split images in the root folder.")

analysis = []
for path in candidates:
    img = Image.open(path)
    mode = img.mode
    has_alpha = "A" in mode
    transparent_pixels = 0
    if has_alpha:
        alpha = np.array(img.convert("RGBA"))[:, :, 3]
        transparent_pixels = int((alpha < 255).sum())
    analysis.append((path, has_alpha, transparent_pixels))

# Pick unit = most transparent pixels
analysis.sort(key=lambda x: x[2], reverse=True)
unit_path, unit_has_alpha, unit_transparent = analysis[0]
background_path, _, _ = analysis[1]

# Save unit as-is (preserve transparency)
unit_img = Image.open(unit_path).convert("RGBA")
unit_img.save(assets / "unit_cutout.png")

# Save background as-is (no edits)
background_img = Image.open(background_path)
background_img.save(assets / "unit_background.png")

print("Unit source:", unit_path)
print("Background source:", background_path)
print("Saved:", assets / "unit_cutout.png")
print("Saved:", assets / "unit_background.png")
print("Unit transparent pixels:", unit_transparent)
