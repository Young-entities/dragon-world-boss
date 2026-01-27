import cv2
import numpy as np
import glob
import os

def surgical_v351_fire_icon_update(output_path):
    # 1. FIND SOURCE (Newest PNG)
    # User says "I set a new icon card".
    files = glob.glob("../*.png") + glob.glob("../*.jpg")
    if not files: 
        print("No source files found!")
        return
    
    # Sort by time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Detected Icon Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None: return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. AUTO-EXTRACT (Just in case)
    # Check if Green Screen
    is_green_dominant = (np.mean(g) > (np.mean(r) + 20)) and (np.mean(g) > (np.mean(b) + 20))
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    
    if is_green_dominant:
        print("Mode: Green Screen Icon")
        is_bg = (g.astype(int) > r.astype(int) + 20) & \
                (g.astype(int) > b.astype(int) + 20) & \
                (g > 50)
        alpha[is_bg] = 0
        # Despill
        max_rb = np.maximum(r, b)
        g = np.minimum(g, max_rb)
    else:
        # Check Black/White
        avg_corner = np.mean([img[0,0], img[0,w-1], img[h-1,0], img[h-1,w-1]], axis=0) # BGR
        B, G, R = avg_corner
        if B < 50 and G < 50 and R < 50:
            print("Mode: Black Screen Icon")
            luma = r.astype(int) + g.astype(int) + b.astype(int)
            is_bg = luma < 50
            alpha[is_bg] = 0
        elif B > 200 and G > 200 and R > 200:
            print("Mode: White Screen Icon")
            # Might need FloodFill for White
            mask = np.zeros((h+2, w+2), np.uint8)
            cv2.floodFill(img, mask, (0,0), (0,0,0), (10,10,10), (10,10,10), 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
            bg_mask = mask[1:h+1, 1:w+1]
            alpha[bg_mask == 255] = 0

    # 3. COMPOSITION (Ensure Square?)
    # Usually icons are square. If source is rectangular (e.g. 16:9), crop center square?
    if w != h:
        print(f"Resizing/Cropping to Square from {w}x{h}...")
        dim = min(w, h)
        cx, cy = w//2, h//2
        x0 = cx - dim//2
        y0 = cy - dim//2
        # Crop
        b = b[y0:y0+dim, x0:x0+dim]
        g = g[y0:y0+dim, x0:x0+dim]
        r = r[y0:y0+dim, x0:x0+dim]
        alpha = alpha[y0:y0+dim, x0:x0+dim]
    
    # Resize to standard icon size (512x512) for consistency?
    # Or keep original resolution if high quality.
    # Let's keep original unless huge.
    
    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V351 Fire Icon Update Complete: {output_path}")

# Target: The Icon file
surgical_v351_fire_icon_update("public/assets/overlord_portrait_v2_clean.png")
