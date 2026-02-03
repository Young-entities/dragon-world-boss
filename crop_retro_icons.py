from PIL import Image
import os
import numpy as np

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
        # Convert to numpy
        arr = np.array(img)
        
        # Calculate brightness (sum RGB)
        rgb = arr[:, :, :3]
        brightness = np.sum(rgb, axis=2)
        
        # Threshold: Increase to 150 to ignore dark gray backgrounds
        mask = brightness > 150

        if not np.any(mask):
            print(f"Image {f} appears empty or too dark.")
            continue
            
        coords = np.argwhere(mask)
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        
        # Padding
        pad = 0 # No padding, we want max size
        
        y0 = max(0, y0 - pad)
        x0 = max(0, x0 - pad)
        y1 = min(img.height, y1 + pad)
        x1 = min(img.width, x1 + pad)
        
        cropped = img.crop((x0, y0, x1, y1))
        
        # Resize to standard size (e.g. 128x128) to ensure consistency? 
        # Or just save as is. CSS handles display size (32x32).
        # We just want to remove the void.
        
        cropped.save(path)
        print(f"Cropped {f} to {x1-x0}x{y1-y0}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
