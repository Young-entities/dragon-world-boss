from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

assets = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets")
cutout = assets / "unit_cutout.png"

img = Image.open(cutout).convert("RGBA")

# Boost brightness and contrast slightly
img = ImageEnhance.Brightness(img).enhance(1.15)
img = ImageEnhance.Contrast(img).enhance(1.2)

# Create glow from alpha
alpha = img.split()[3]
mask = alpha.filter(ImageFilter.MaxFilter(7))
mask = mask.filter(ImageFilter.GaussianBlur(6))

glow_color = (255, 120, 20, 180)
glow = Image.new("RGBA", img.size, glow_color)

glow.putalpha(mask)

# Composite glow behind original
base = Image.new("RGBA", img.size, (0, 0, 0, 0))
base = Image.alpha_composite(base, glow)
base = Image.alpha_composite(base, img)

out = assets / "unit_cutout_visible.png"
base.save(out)
print(f"Saved enhanced cutout: {out}")
