from PIL import Image, ImageDraw
import numpy as np

# Inputs
screenshot_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1770122213729.png"
button_path = "public/assets/stat_stamina_retro.png"

# Load Screenshot (Pixel Sword Source)
try:
    src_img = Image.open(screenshot_path).convert("RGBA")
    
    # 1. Extract the Sword (Crop Center)
    # The screenshot seems zoomed in on the sword.
    # Let's crop the center 50% just to focus.
    w, h = src_img.size
    crop_img = src_img.crop((w//4, h//4, 3*w//4, 3*h//4))
    
    # 2. Remove Background (Dark Theme)
    # Background color is ~ (20, 25, 35)
    # Sword is Grey, White, Orange.
    # Logic: Keep pixels that are bright OR orange.
    arr = np.array(crop_img)
    # Don't use Transpose for channel access, it flips Width/Height
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    # Brightness mask (Grey/White)
    brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3
    mask_bright = brightness > 60
    
    # Orange mask (R > B + 30)
    mask_orange = (r > b + 20) & (r > 60)
    
    final_mask = mask_bright | mask_orange
    
    # Apply alpha
    arr[:, :, 3] = np.where(final_mask, 255, 0)
    
    sword_transparent = Image.fromarray(arr)
    
    # Trim transparency
    bbox = sword_transparent.getbbox()
    if bbox:
        sword_transparent = sword_transparent.crop(bbox)
        
    # Scale up? It's pixel art.
    # We want it to be ~500px in the 1024px button.
    # Current size is tiny (e.g. 20x20).
    target_size = 500
    if sword_transparent.width > 0:
        ratio = target_size / sword_transparent.width
        new_w = int(sword_transparent.width * ratio)
        new_h = int(sword_transparent.height * ratio)
        # NEAREST NEIGHBOR to keep pixels
        sword_scaled = sword_transparent.resize((new_w, new_h), Image.NEAREST)
        
    # Load Button (Glossy Source)
    bg_img = Image.open(button_path).convert("RGBA")
    
    # Erase center (Draw Maroon Circle)
    # Sample color from corner
    bg_color = bg_img.getpixel((50, 50)) 
    # Or hardcode if sample fails (it might be neon glow).
    # Center color is usually dark maroon.
    center_color = bg_img.getpixel((bg_img.width//2, bg_img.height//2)) # This is the sword color! Don't sample center.
    
    # Use hardcoded Maroon from previous generations or sample safely
    # (40, 0, 10)?
    # Better: Use the color at (width/4, height/4) which is background.
    safe_bg = bg_img.getpixel((bg_img.width//4, bg_img.height//4))
    
    draw = ImageDraw.Draw(bg_img)
    # Draw circle to cover old swords
    cx, cy = bg_img.width//2, bg_img.height//2
    rad = bg_img.width//2 - 60 # Stay inside border
    # Wait, 'rad' covers the whole button. We just want to cover the swords.
    # Swords are in center.
    draw.rectangle([(100, 100), (bg_img.width-100, bg_img.height-150)], fill=safe_bg)
    # Maybe oval?
    
    # Paste Pixel Sword
    offset_x = (bg_img.width - sword_scaled.width) // 2
    offset_y = (bg_img.height - sword_scaled.height) // 2
    
    bg_img.alpha_composite(sword_scaled, (offset_x, offset_y))
    
    bg_img.save(button_path)
    print("Composited Pixel Sword into Glossy Button.")

except Exception as e:
    print(f"Error: {e}")
