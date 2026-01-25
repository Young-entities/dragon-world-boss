from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np

root = Path(r"C:\Users\kevin\New folder (2)")
assets = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets")
assets.mkdir(parents=True, exist_ok=True)

files = sorted(root.glob("Gemini_Generated_Image_*.png"))
if len(files) < 2:
    raise SystemExit("Need two Gemini split images in the root folder.")

scored = []
for path in files:
    img = Image.open(path).convert("RGBA")
    cutout = remove(img)
    alpha = np.array(cutout)[:, :, 3]
    score = int((alpha > 0).sum())
    scored.append((score, path, cutout))

scored.sort(reverse=True, key=lambda x: x[0])
unit_score, unit_path, unit_cutout = scored[0]
background_path = scored[1][1]

unit_cutout.save(assets / "unit_cutout.png")
Image.open(background_path).save(assets / "unit_background.png")

print("Unit source:", unit_path)
print("Background source:", background_path)
print("Unit alpha pixels:", unit_score)
print("Saved unit_cutout.png and unit_background.png")
