import cv2
import numpy as np
import glob
import os

def surgical_v110_ice_flip(output_path):
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
    
    # 2. RAW EXTRACTION (V106 Base)
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. BLACK LINE RECOLOR (V108 Base)
    is_dark_line = (brightness < 80) & (alpha == 255)
    
    # Modify RGB channels
    new_b = b.copy()
    new_g = g.copy()
    new_r = r.copy()
    
    # Recolor Black to Dark Blue
    new_b[is_dark_line] = 100
    new_g[is_dark_line] = 40
    new_r[is_dark_line] = 0
    
    # 4. ORANGE FLIP (New Logic)
    # Instead of deleting orange (jagged), we flip it to Blue.
    
    # Narrow Skin Zone (Protection)
    col_x0, col_x1 = int(w*0.43), int(w*0.57) # Very narrow center
    col_y0, col_y1 = int(h*0.20), int(h*0.55)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    # Warm detection: R > B (Even slightly warm)
    is_warm = (new_r > new_b)
    
    should_flip = is_warm & (~in_skin_zone) & (alpha == 255)
    
    # Action: Swap R and B channels for these pixels.
    # Orange (High R, Low B) -> Blue (High B, Low R)
    temp_r = new_r[should_flip]
    temp_b = new_b[should_flip]
    
    new_r[should_flip] = temp_b
    new_b[should_flip] = temp_r
    
    # 5. SHAVE (2px)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # 6. ARTIFACT CLEANUP
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([new_b, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V110 Ice Flip Complete: {output_path}")

surgical_v110_ice_flip("public/assets/water_deity_unit_final.png")
