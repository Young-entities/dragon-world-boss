import cv2
import numpy as np
import glob
import os

def surgical_v360_deity_icon(output_path):
    # 1. FIND SOURCE (Newest PNG)
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
    
    # 2. AUTO-EXTRACT
    # Check Green Screen
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
            is_bg = luma < 60
            alpha[is_bg] = 0
        elif B > 200 and G > 200 and R > 200:
            print("Mode: White Screen Icon")
            mask = np.zeros((h+2, w+2), np.uint8)
            cv2.floodFill(img, mask, (0,0), (0,0,0), (10,10,10), (10,10,10), 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
            bg_mask = mask[1:h+1, 1:w+1]
            alpha[bg_mask == 255] = 0
        else:
            print("Mode: Complex Icon (Assuming Transparent or Crop)")
            # If PNG has alpha, use it. But imread defaults to BGR.
            # Try reloading with Alpha
            img_alpha = cv2.imread(latest_file, cv2.IMREAD_UNCHANGED)
            if img_alpha.shape[2] == 4:
                print("Using existing Alpha channel")
                alpha = img_alpha[:,:,3]
    
    # 3. SQUARE CROP
    if w != h:
        print(f"Resizing/Cropping to Square from {w}x{h}...")
        dim = min(w, h)
        cx, cy = w//2, h//2
        x0 = cx - dim//2
        y0 = cy - dim//2
        b = b[y0:y0+dim, x0:x0+dim]
        g = g[y0:y0+dim, x0:x0+dim]
        r = r[y0:y0+dim, x0:x0+dim]
        alpha = alpha[y0:y0+dim, x0:x0+dim]

    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V360 Deity Icon Complete: {output_path}")

surgical_v360_deity_icon("public/assets/water_deity_icon_clean.png")
