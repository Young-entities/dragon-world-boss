from PIL import Image
import os

files = [
    "public/assets/stat_hp_retro.png",
    "public/assets/stat_stamina_retro.png"
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
        
        # Crop to the center 75% to remove outer padding/glow
        crop_ratio = 0.75
        new_width = int(width * crop_ratio)
        new_height = int(height * crop_ratio)
        
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        
        cropped = img.crop((left, top, right, bottom))
        
        cropped.save(path)
        print(f"Zoomed {f} (Cropped to 75% center): {width}x{height} -> {new_width}x{new_height}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
