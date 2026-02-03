from PIL import Image
import os

files = [
    "public/assets/stat_hp_retro.png",
    "public/assets/stat_energy_retro.png",
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
        
        # Determine square size (use minimum dimension)
        # This assumes the crucial content is centered and square-ish
        # and the excess in the larger dimension is noise/background.
        size = min(width, height)
        
        # Calculate center crop
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        
        cropped = img.crop((left, top, right, bottom))
        
        cropped.save(path)
        print(f"Squarified {f}: {width}x{height} -> {size}x{size}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
