import cv2
import numpy as np
import glob
import os

def surgical_v108_recolor(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. RAW EXTRACTION
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. BLACK LINE RECOLORING (The "Un-Sticker" Move)
    # Instead of deleting the black lines (which ruins the shape), we dye them Blue.
    # Logic: If pixel is opaque AND Dark (< 80 brightness), set it to Dark Blue.
    
    is_dark_line = (brightness < 80) & (alpha == 255)
    
    # Set to Dark Blue (BGR: 100, 40, 0) - Deep Cyan/Blue
    # We modify the RGB channels directly.
    # Only modify where is_dark_line is True
    
    # Make a copy of channels to modify
    new_b = b.copy()
    new_g = g.copy()
    new_r = r.copy()
    
    new_b[is_dark_line] = 100
    new_g[is_dark_line] = 40
    new_r[is_dark_line] = 0
    
    # 4. ORANGE KILLER (Refined)
    col_x0, col_x1 = int(w*0.42), int(w*0.58) # Narrower Skin Zone (42-58%)
    col_y0, col_y1 = int(h*0.20), int(h*0.50) # Only upper body
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    # Stricter Warm definition: Red is significantly higher than Blue
    is_warm = (r.astype(int) > b.astype(int) + 10)
    should_kill_orange = is_warm & (~in_skin_zone) & (alpha == 255)
    
    alpha[should_kill_orange] = 0

    # 5. STANDARD SHAVE (2px)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # 6. ARTIFACT CLEANUP
    alpha[0:50, 0:50] = 0
    
    # Save (Combine modified channels)
    final_img = cv2.merge([new_b, new_g, new_r, alpha])
    
    # Clean transparent pixels
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V108 Recolor Complete: {output_path}")

surgical_v108_recolor("public/assets/water_deity_unit_final.png")
