from pathlib import Path
from PIL import Image
import numpy as np

assets = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets")
cutout = assets / "unit_cutout.png"
background = assets / "unit_background.png"

print("cutout exists:", cutout.exists(), "background exists:", background.exists())

if cutout.exists():
    img = Image.open(cutout).convert("RGBA")
    alpha = np.array(img)[:, :, 3]
    nonzero = np.argwhere(alpha > 0)
    if nonzero.size:
        y0, x0 = nonzero.min(axis=0)
        y1, x1 = nonzero.max(axis=0)
        bbox = (int(x0), int(y0), int(x1), int(y1))
        print("cutout bbox:", bbox)
    else:
        print("cutout alpha is empty")

    w, h = img.size
    tile = 32
    checker = Image.new("RGBA", (w, h), (200, 200, 200, 255))
    pixels = checker.load()
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            if (x // tile + y // tile) % 2 == 0:
                for yy in range(y, min(y + tile, h)):
                    for xx in range(x, min(x + tile, w)):
                        pixels[xx, yy] = (235, 235, 235, 255)
    preview = Image.alpha_composite(checker, img)
    preview_path = assets / "unit_cutout_preview.png"
    preview.save(preview_path)
    print("saved preview:", preview_path)
