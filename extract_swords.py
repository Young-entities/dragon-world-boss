from PIL import Image
import os
import numpy as np
import colorsys

source = "public/assets/stat_stamina_retro.png"
dest = "public/assets/icon_battle.png"
base_dir = r"c:\Users\kevin\New folder (2)\monster-warlord"

src_path = os.path.join(base_dir, source)
dest_path = os.path.join(base_dir, dest)

if os.path.exists(src_path):
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)
    
    # Logic: Extract the Blue Swords
    # Background is Dark Maroon. Swords are Bright Blue.
    # Convert to float for easier logic
    r, g, b, a = arr.T
    
    # Condition: Blue is dominant
    # Blue > Red + 20 AND Blue > Green - 50?
    # Simple Brightness + Blue dominance
    
    # Mask 1: Significant Blue component
    blue_mask = (b > r) & (b > 50)
    
    # Mask 2: Brightness (ignore dark background)
    brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3
    bright_mask = brightness > 40
    
    mask = blue_mask & bright_mask
    
    # Create new alpha channel
    new_alpha = np.zeros_like(a)
    new_alpha[mask] = 255
    
    # Apply mask to image
    res = arr.copy()
    res[:, :, 3] = new_alpha
    
    # Re-Crop to tight bounding box
    final_img = Image.fromarray(res)
    bbox = final_img.getbbox()
    if bbox:
        final_img = final_img.crop(bbox)
        
    final_img.save(dest_path)
    print(f"Extracted Swords to {dest}")
else:
    print("Source stamina icon not found")
