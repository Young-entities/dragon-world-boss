import cv2
import numpy as np
import glob
import os

def surgical_v201_right_fix(output_path):
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
    # Standard Despill: Clamp Green to max(Red, Blue)
    new_g = np.minimum(new_g, max_rb)
    
    # 4. RIGHT SIDE FIX (Aggressive)
    # User complained about "the right side".
    # Focusing on the right half (Dragons).
    
    # Zone: x > 50%
    right_side = np.zeros_like(alpha, dtype=bool)
    right_side[:, int(w*0.5):] = True
    
    # Fix 1: Stricter Despill on Right
    # Clamp Green STRICTLY to Blue (since it's ice).
    # If G > B on the right side, clamp it.
    current_g = new_g[right_side]
    current_b = b[right_side]
    new_g[right_side] = np.minimum(current_g, current_b)
    
    # Fix 2: Extra Shave on Right Edge
    # Often green screens leave a 1px halo on complex shapes (dragons).
    # We will erode ONLY the right side?
    # Hard to erode 'only right side' without mask boundaries.
    # Let's apply Global Erode 1px (Standard)
    # And then a SECOND Erode 1px on the Right Half Mask?
    
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1) # Global 1px
    
    # Create mask for Right Side clean
    # Crop alpha to right side
    right_alpha = alpha[:, int(w*0.5):]
    # Erode it again
    right_alpha_eroded = cv2.erode(right_alpha, kernel, iterations=1)
    # Paste back
    alpha[:, int(w*0.5):] = right_alpha_eroded
    
    # 5. ORANGE KILLER (Standard)
    col_x0, col_x1 = int(w*0.43), int(w*0.57) 
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)

    # 6. SHADOW LIFT (Dark Blue)
    brightness = new_r.astype(int) + new_g.astype(int) + b.astype(int)
    is_very_dark = (brightness < 60) & (alpha == 255)
    new_b_out = b.copy()
    new_b_out[is_very_dark] = 100 

    # Save
    final_img = cv2.merge([new_b_out, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V201 Right Fix Complete: {output_path}")

surgical_v201_right_fix("public/assets/water_deity_unit_final.png")
