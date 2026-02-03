from PIL import Image
import os

files = [
    "public/assets/stat_attack_modern.png",
    "public/assets/stat_defense_modern.png",
    "public/assets/stat_overdrive_modern.png"
]

base_dir = r"c:\Users\kevin\New folder (2)\monster-warlord"

for f in files:
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        print(f"Skipping {f}, not found")
        continue

    try:
        img = Image.open(path).convert("RGBA")
        width, height = img.size
        
        # Crop to Center 75% (Matches scale of HP/ST)
        crop_factor = 0.75
        new_w = int(width * crop_factor)
        new_h = int(height * crop_factor)
        
        left = (width - new_w) // 2
        top = (height - new_h) // 2
        right = left + new_w
        bottom = top + new_h
        
        cropped = img.crop((left, top, right, bottom))
        
        cropped.save(path)
        print(f"Processed {f}: {width}x{height} -> {new_w}x{new_h}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
