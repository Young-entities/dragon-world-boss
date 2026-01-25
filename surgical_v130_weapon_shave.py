import cv2
import numpy as np
import glob
import os

def surgical_v130_weapon_shave(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    
    # 2. RAW EXTRACTION (V120 Base)
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. NUCLEAR WINTER (Kill Orange - V120 Base)
    h, w = img.shape[:2]
    col_x0, col_x1 = int(w*0.43), int(w*0.57)
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    # Clamp Red to Blue (No Warmth)
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)
    
    # 4. BLUE SHADOWS (Global)
    new_b = b.copy()
    is_very_dark = (brightness < 60) & outside_skin
    new_b[is_very_dark] = 100 # Dark Blue Shadows on body
    
    # 5. WEAPON SHAVE (The Fix)
    # User specifically hates the black outline on the weapon.
    # We will ERODE the weapon area significantly more than the body.
    
    # Global Erode (2px - Standard)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # Weapon Erode (Extra 3px -> Total 5px)
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.45) # Widened box slightly to ensure tip coverage
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    spear_part = np.zeros_like(alpha)
    spear_part[in_spear_box] = alpha[in_spear_box]
    
    # 3 extra iterations on the spear tip
    spear_shaved = cv2.erode(spear_part, kernel, iterations=3) 
    
    # Replace spear part in alpha
    alpha[in_spear_box] = spear_shaved[in_spear_box]

    # Artifact Clean
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([new_b, g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V130 Weapon Shave Complete: {output_path}")

surgical_v130_weapon_shave("public/assets/water_deity_unit_final.png")
