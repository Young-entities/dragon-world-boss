from PIL import Image
import os
import numpy as np

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
        arr = np.array(img)
        
        # Calculate brightness
        rgb = arr[:, :, :3]
        brightness = np.sum(rgb, axis=2)
        
        # Threshold: look for the Neon Border (Bright)
        # Background is dark maroon (~20-50 sum)
        # Border is Neon (>200 sum)
        # Threshold 100 should be safe.
        mask = brightness > 100

        if not np.any(mask):
            print(f"Image {f} is dark.")
            continue
            
        coords = np.argwhere(mask)
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        
        # Add small padding to avoid cutting the glow harshly
        padding = 5
        y0 = max(0, y0 - padding)
        x0 = max(0, x0 - padding)
        y1 = min(img.height, y1 + padding)
        x1 = min(img.width, x1 + padding)
        
        cropped = img.crop((x0, y0, x1, y1))
        
        # Also ensure it's square-ish (optional, but good for UI)
        # If I crop to border, it should be roughly square for these icons.
        
        cropped.save(path)
        print(f"Fixed Crop {f}: {img.width}x{img.height} -> {x1-x0}x{y1-y0}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")
