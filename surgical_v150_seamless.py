import cv2
import numpy as np
import glob
import os

def surgical_v150_seamless(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. RAW EXTRACTION (V120 Base)
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. NUCLEAR WINTER (Kill Orange)
    col_x0, col_x1 = int(w*0.43), int(w*0.57)
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)
    
    # 4. SEAMLESS OUTLINE GLOW (The Fix)
    # Instead of a box, we apply this everywhere (except face).
    # Instead of Flat Color, we Lighten shadows.
    
    # Detect Face/Eyes to protect their black color
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    
    # Condition: Dark Pixel AND Not in Face AND Not Background
    is_dark = (brightness < 80) & (alpha == 255)
    should_brighten = is_dark & (~in_face_box)
    
    new_b = b.copy()
    new_g = g.copy()
    
    # Action: Set to Luminous Cyan (Not white, not black)
    # B=220, G=180, R=New_R (which is < B, so Low red)
    new_b[should_brighten] = 220
    new_g[should_brighten] = 180
    
    # 5. SHAVE (2px)
    # Standard clean edge. No 5px blunt cut.
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # Artifact Clean
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([new_b, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V150 Seamless Complete: {output_path}")

surgical_v150_seamless("public/assets/water_deity_unit_final.png")
