from PIL import Image, ImageFilter
import numpy as np

src_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1770122633438.png"
btn_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/blank_cyan_button_1770122481004.png"
dest_path = "public/assets/stat_stamina_retro.png"

try:
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)
    
    # Intelligently remove checkerboard
    # Sample top-left and top-left+offset (to catch both check colors)
    c1 = arr[0,0]
    c2 = arr[0,10] # Assume square size is > 1
    # Or just sample random corners
    
    # Identify background colors
    # Let's assume background colors are frequent in the border area
    border_pixels = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
    # Find unique colors
    unique_colors, counts = np.unique(border_pixels.reshape(-1, 4), axis=0, return_counts=True)
    
    # Create mask: Start transparent (0)
    # Any pixel NOT matching a background color is Opaque (255)
    
    # Function to check difference
    def color_dist(c1, c2):
        return np.sum(np.abs(c1 - c2), axis=2)

    # Allow tolerance for compression?
    # Create a mask of "Keep"
    keep_mask = np.ones(arr.shape[:2], dtype=bool)
    
    # Sort background colors by frequency
    sorted_indices = np.argsort(counts)[::-1]
    top_bg_colors = unique_colors[sorted_indices][:5] # Top 5 border colors
    
    rgb = arr[:, :, :3]
    
    for bg in top_bg_colors:
        # Distance from this bg color
        bg_rgb = bg[:3]
        dist = np.sum(np.abs(rgb - bg_rgb), axis=2)
        # If close to background, set Keep to False
        is_bg = dist < 15
        keep_mask[is_bg] = False
        
    # Apply mask
    arr[:, :, 3] = np.where(keep_mask, 255, 0)
    
    # 2. Smooth Mask (Antialias)
    extracted = Image.fromarray(arr)
    # Get alpha
    alpha = extracted.split()[3]
    # Small box blur on alpha to soften edges?
    # alpha = alpha.filter(ImageFilter.BoxBlur(1))
    # extracted.putalpha(alpha)
    
    # Crop
    bbox = extracted.getbbox()
    if bbox:
        extracted = extracted.crop(bbox)
        
    # 3. Apply Effects (Fake 3D/Gloss)
    # A. Drop Shadow
    shadow = Image.new("RGBA", extracted.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    # Draw silhouette
    shadow_draw.bitmap((0, 0), extracted.split()[3], fill=(0, 0, 0, 100))
    # Blur
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    
    # B. Gloss Overlay (Top Shine)
    gloss = Image.new("RGBA", extracted.size, (255, 255, 255, 0))
    # Create gradient mask
    g_mask = Image.new("L", extracted.size, 0)
    g_draw = ImageDraw.Draw(g_mask)
    # Linear gradient top to bottom
    for y in range(extracted.height):
        # Alpha 150 at top, 0 at middle
        alpha_val = int(255 * (1 - (y / (extracted.height * 0.6))))
        alpha_val = max(0, min(255, alpha_val))
        # Scanline
        g_draw.line([(0, y), (extracted.width, y)], fill=alpha_val)
    
    # Mask gloss by sword alpha
    gloss.putalpha(ImageChops.multiply(g_mask, extracted.split()[3]))
    
    # 4. Composite
    btn = Image.open(btn_path).convert("RGBA")
    
    # Resize Sword Group (70% of btn)
    target_dim = int(min(btn.size) * 0.70)
    
    if extracted.width > 0:
        ratio = target_dim / max(extracted.size)
        new_size = (int(extracted.width * ratio), int(extracted.height * ratio))
        
        extracted_res = extracted.resize(new_size, Image.Resampling.LANCZOS)
        shadow_res = shadow.resize(new_size, Image.Resampling.LANCZOS)
        gloss_res= gloss.resize(new_size, Image.Resampling.LANCZOS) # Correction: Apply resize to gloss too
        
        # Paste Center
        bx, by = btn.size
        sx, sy = extracted_res.size
        offset = ((bx - sx)//2, (by - sy)//2)
        shadow_offset = (offset[0], offset[1] + 5)
        
        # Composite Order: Button -> Shadow -> Sword -> Gloss
        btn.alpha_composite(shadow_res, shadow_offset)
        btn.alpha_composite(extracted_res, offset)
        btn.alpha_composite(gloss_res, offset)
        
        btn.save(dest_path)
        print("Composited Vector Sword (Smart Clean + Gloss Effects) into Button.")
        
except Exception as e:
    print(f"Error: {e}")
