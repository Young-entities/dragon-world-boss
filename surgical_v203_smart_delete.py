import cv2
import numpy as np
import glob
import os

def surgical_v203_smart_delete(output_path):
    # 1. Source (Green Screen)
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. RAW GREEN EXTRACTION (V200 Base)
    # G > R + 20 and G > B + 20 and G > 50
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # 3. DESPILL (Global)
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb)
    
    # 4. RIGHT SIDE FIX (V201 Despill Logic but NO HARD CROP)
    right_side = np.zeros_like(alpha, dtype=bool)
    right_side[:, int(w*0.5):] = True
    current_g = new_g[right_side]
    current_b = b[right_side]
    new_g[right_side] = np.minimum(current_g, current_b)
    
    # 5. SMART BAR REMOVAL (The Fix)
    # Instead of cropping 15% blind (which cuts the dragon),
    # we target the specific "Black Bar" artifact.
    # Logic: Only delete pixels on the far right if they are DARK.
    
    secure_zone_x = int(w * 0.80)
    brightness = new_r.astype(int) + new_g.astype(int) + b.astype(int)
    
    # Identify the artifact: Far Right AND Dark
    is_artifact = (brightness < 50) # Very Dark
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    
    # Remove
    alpha[is_artifact & is_far_right] = 0

    # 6. ORANGE KILLER (Standard)
    col_x0, col_x1 = int(w*0.43), int(w*0.57) 
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)

    # 7. SHADOW LIFT (Standard)
    brightness = new_r.astype(int) + new_g.astype(int) + b.astype(int)
    is_very_dark = (brightness < 60) & (alpha == 255)
    new_b_out = b.copy()
    new_b_out[is_very_dark] = 100 

    # Save
    final_img = cv2.merge([new_b_out, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V203 Smart Delete Complete: {output_path}")

surgical_v203_smart_delete("public/assets/water_deity_unit_final.png")
