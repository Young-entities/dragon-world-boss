from PIL import Image, ImageOps
import numpy as np

# Inputs
src_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1770122633438.png"
btn_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/blank_cyan_button_1770122481004.png"
dest_path = "public/assets/stat_stamina_retro.png"

try:
    # 1. Process Source (Vector Sword)
    raw_img = Image.open(src_path).convert("RGBA")
    
    # Check if transparent
    arr = np.array(raw_img)
    alpha = arr[:,:,3]
    
    # If image is fully opaque (screenshot), remove background
    if np.min(alpha) == 255:
        print("Image is opaque. Attempting background removal...")
        rgb = arr[:,:,:3]
        # Heuristic: Background is likely dark or checkerboard.
        # Sword is Grey/White/Orange.
        # Calculate distance from 'content' colors?
        # Simpler: Flood fill from corners?
        # Let's try simple brightness/color keying.
        # Checkerboard is Grey(128) and Dark(50)?
        # Content is Bright White/Grey and Orange.
        
        # Keep pixels that are:
        # 1. Very bright (Blades) -> Sum > 400?
        # 2. Orange (Hilt/Sparks) -> R > B+30
        
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        
        mask_bright = brightness > 350
        mask_orange = (r > b + 30) & (r > 60)
        
        mask = mask_bright | mask_orange
        
        # Clean up noise?
        # Apply mask
        arr[:,:,3] = np.where(mask, 255, 0)
        
        sword_img = Image.fromarray(arr)
        # Crop to content
        bbox = sword_img.getbbox()
        if bbox:
            sword_img = sword_img.crop(bbox)
    else:
        # Already transparent
        sword_img = raw_img
        bbox = sword_img.getbbox()
        if bbox:
            sword_img = sword_img.crop(bbox)

    # 2. Load Button
    btn_img = Image.open(btn_path).convert("RGBA")
    
    # 3. Resize Sword to fit
    # Target: 70% of button size
    target_w = int(btn_img.width * 0.70)
    target_h = int(btn_img.height * 0.70)
    
    # Aspect fit
    ratio = min(target_w / sword_img.width, target_h / sword_img.height)
    new_size = (int(sword_img.width * ratio), int(sword_img.height * ratio))
    
    sword_resized = sword_img.resize(new_size, Image.Resampling.LANCZOS)
    
    # 4. Composite (Center)
    bg_w, bg_h = btn_img.size
    fg_w, fg_h = sword_resized.size
    offset = ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2)
    
    btn_img.alpha_composite(sword_resized, offset)
    
    # 5. Save
    btn_img.save(dest_path)
    print(f"Composited Vector Sword into Button. Saved to {dest_path}")
    
except Exception as e:
    print(f"Error: {e}")
