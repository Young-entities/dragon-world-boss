from PIL import Image
import os

# Only fixing HP and Stamina (Energy is good)
files_config = [
    {"path": "public/assets/stat_hp_retro.png", "crop": 0.85},     # Zoom in another 15%
    {"path": "public/assets/stat_stamina_retro.png", "crop": 0.80} # Zoom in another 20%
]

base_dir = r"c:\Users\kevin\New folder (2)\monster-warlord"

for item in files_config:
    f = item["path"]
    crop_ratio = item["crop"]
    
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        print(f"Skipping {f}, not found")
        continue

    try:
        img = Image.open(path).convert("RGBA")
        width, height = img.size
        
        # Calculate new crop dimensions
        new_width = int(width * crop_ratio)
        new_height = int(height * crop_ratio)
        
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        
        cropped = img.crop((left, top, right, bottom))
        
        cropped.save(path)
        print(f"Zoomed More {f} (Crop {crop_ratio}): {width}x{height} -> {new_width}x{new_height}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
