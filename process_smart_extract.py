import cv2
import numpy as np

def surgical_v75_smart_extract(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: 
        print(f"Could not load {input_path}")
        return
    
    # 1. Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- SMART LOGIC V76 (Corrected) ---
    
    # 1. Global Background Definition (Strict)
    # Bright (>210) and Low Saturation (<30). 
    # This guarantees the general white background is nuked.
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    is_bg = (luma > 210) & (saturation < 30)
    
    # Initialize Alpha: Default to Opaque, set BG to Transparent
    alpha = np.ones_like(luma, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # --- PROTECTION ZONES (The Exceptions) ---
    h_idx, w_idx = np.indices((h, w))
    
    # 1. WEAPON ZONE (Ice Protection)
    # Only in the weapon area do we allow "Bright" things to survive if they are "Blueish"
    # Spear tip is bright white/blue.
    weapon_y_min, weapon_y_max = int(h*0.50), int(h*0.90)
    weapon_x_min, weapon_x_max = int(w*0.0), int(w*0.45)
    in_weapon_box = (h_idx >= weapon_y_min) & (h_idx <= weapon_y_max) & \
                    (w_idx >= weapon_x_min) & (w_idx <= weapon_x_max)
    
    # Logic: If inside weapon box AND (Blue > Red), keep it (even if bright/low sat).
    # Ice highlights usually have B > R. Background noise usually R ~= B.
    is_ice = (b > r) 
    weapon_save = in_weapon_box & is_ice
    alpha[weapon_save] = 255

    # 2. FACE ZONE (Absolute Protection)
    face_y_min, face_y_max = int(h*0.20), int(h*0.35)
    face_x_min, face_x_max = int(w*0.42), int(w*0.58)
    in_face_box = (h_idx >= face_y_min) & (h_idx <= face_y_max) & \
                  (w_idx >= face_x_min) & (w_idx <= face_x_max)
    alpha[in_face_box] = 255
    
    # 3. SKIN ZONE (Center Column Protection)
    center_x_min, center_x_max = int(w*0.30), int(w*0.70)
    in_body_col = (w_idx >= center_x_min) & (w_idx <= center_x_max)
    is_skin = (r > g) & (g > b) & (r > 150)
    skin_save = in_body_col & is_skin
    alpha[skin_save] = 255

    # --- EDGE CLEANING ---
    # Erode to kill fringe
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    rgba[:,:,3] = alpha
    rgba[alpha == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Smart Extraction V76 Complete: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v75_smart_extract(source, "public/assets/water_deity_unit_final.png")
