from PIL import Image
import os

f = "public/assets/stat_stamina_retro.png"
base_dir = r"c:\Users\kevin\New folder (2)\monster-warlord"
path = os.path.join(base_dir, f)

if os.path.exists(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    # Crop to Center 75% (Matches HP/Energy scale)
    # Assumes GenAI output is 1024x1024 with centered content
    crop_factor = 0.75
    new_w = int(w * crop_factor)
    new_h = int(h * crop_factor)
    
    left = (w - new_w) // 2
    top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h
    
    cropped = img.crop((left, top, right, bottom))
    cropped.save(path)
    print(f"Finalized Stamina Icon: {w}x{h} -> {new_w}x{new_h}")
else:
    print("File not found.")
