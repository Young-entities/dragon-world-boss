from PIL import Image
import os
import numpy as np

files = [
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
        arr = np.array(img)
        
        # Calculate brightness
        rgb = arr[:, :, :3]
        brightness = np.sum(rgb, axis=2)
        
        # Threshold: Increase to 200 to ignore maroon background
        # Only capture the bright Neon Border and Icon Content
        mask = brightness > 200

        if not np.any(mask):
            print(f"Image {f} is too dark for threshold 200.")
            continue
            
        coords = np.argwhere(mask)
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        
        # Add small padding
        padding = 5
        y0 = max(0, y0 - padding)
        x0 = max(0, x0 - padding)
        y1 = min(img.height, y1 + padding)
        x1 = min(img.width, x1 + padding)
        
        cropped = img.crop((x0, y0, x1, y1))
        
        cropped.save(path)
        print(f"Fixed Crop (Threshold 200) {f}: {img.width}x{img.height} -> {x1-x0}x{y1-y0}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
