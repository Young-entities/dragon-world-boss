import cv2
import numpy as np
import glob
import os

def surgical_v140_weapon_bleach(output_path):
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
    
    # 3. NUCLEAR WINTER (Kill Orange - V120 Base)
    col_x0, col_x1 = int(w*0.43), int(w*0.57)
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)
    
    # 4. BLUE SHADOWS (Global)
    new_b = b.copy()
    new_g = g.copy()
    is_very_dark = (brightness < 60) & outside_skin
    new_b[is_very_dark] = 100 
    
    # 5. WEAPON BLEACH (The Fix)
    # User wants "all the black to go off the weapon".
    # Shaving edges wasn't enough because the shading INSIDE is dark.
    # We must RE-LIGHT the weapon.
    
    spear_y0, spear_y1 = int(h*0.55), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.50) # Wide coverage
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    # Condition: Inside Spear Box AND Dark
    # luma < 120 (Mid-tones and Shadows)
    luma = 0.299*r + 0.587*g + 0.114*b
    is_spear_shadow = in_spear_box & (luma < 120) & (alpha == 255)
    
    # Action: Turn Shadows into Bright Cyan Ice
    # B=255, G=200, R=50
    new_b[is_spear_shadow] = 255
    new_g[is_spear_shadow] = 200
    new_r[is_spear_shadow] = 50
    
    # Also force the previously "Blue Shadow" pixels in the spear to be Bright too
    # (Since step 4 might have set them to 100)
    
    # 6. SHAVE (2px)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # Spear Shave (3px extra - keeps the edge clean)
    spear_part = np.zeros_like(alpha)
    spear_part[in_spear_box] = alpha[in_spear_box]
    spear_shaved = cv2.erode(spear_part, kernel, iterations=3) 
    alpha[in_spear_box] = spear_shaved[in_spear_box]

    # Artifact Clean
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([new_b, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V140 Weapon Bleach Complete: {output_path}")

surgical_v140_weapon_bleach("public/assets/water_deity_unit_final.png")
