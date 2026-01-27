import cv2
import numpy as np
import glob
import os

def surgical_v304_fire_sidebar(output_path):
    # 1. SOURCE
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    latest_file = files[0] if files else None
    
    # Fallback to general search if targeted file fails (rare)
    if not latest_file:
         return 

    print(f"Using Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. SATURATION EXTRACTION (V303 Base)
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    
    is_bg = (saturation < 30) & (brightness < 120)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. SAFETY ZONES (V303 Base)
    head_x0, head_x1 = int(w*0.4), int(w*0.6)
    head_y0, head_y1 = int(h*0.1), int(h*0.3)
    head_mask = np.zeros_like(alpha, dtype=bool)
    head_mask[head_y0:head_y1, head_x0:head_x1] = True
    
    legs_x0, legs_x1 = int(w*0.3), int(w*0.7)
    legs_y0, legs_y1 = int(h*0.6), int(h*0.95)
    legs_mask = np.zeros_like(alpha, dtype=bool)
    legs_mask[legs_y0:legs_y1, legs_x0:legs_x1] = True
    
    should_save = (head_mask | legs_mask) & (brightness < 60)
    alpha[should_save] = 255
    
    # 4. SIDEBAR CLEAN (The Fix)
    # User sees a Black Bar on the Right.
    # Logic: Delete DARK pixels on the far Right.
    # Secure Zone: x > 85%.
    
    secure_zone_x = int(w * 0.85)
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    
    # If pixel is Dark (< 60 brightness) and on Far Right -> Delete.
    # Fire Sword Tip is bright/saturated, so it is safe.
    
    is_artifact = (brightness < 100) # Slightly aggressive on "Dark" meaning
    alpha[is_artifact & is_far_right] = 0
    
    # 5. POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Clean Corners
    corner = 20
    alpha[0:corner, 0:corner] = 0
    alpha[0:corner, -corner:] = 0
    alpha[-corner:, 0:corner] = 0
    alpha[-corner:, -corner:] = 0

    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V304 Fire Sidebar Complete: {output_path}")

surgical_v304_fire_sidebar("public/assets/overlord_absolute_final.png")
