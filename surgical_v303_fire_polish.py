import cv2
import numpy as np
import glob
import os

def surgical_v303_fire_polish(output_path):
    # 1. SOURCE (Targeted)
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    if not files: return
    latest_file = files[0]
    print(f"Using Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. SATURATION EXTRACTION
    # Fire/Red units are High Saturation.
    # Black/Dark backgrounds are Low Saturation.
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    
    # Condition: Is Background?
    # Low Saturation (< 30) AND Low Brightness (< 100)
    # (Allowing slightly brighter grey background to be removed)
    is_bg = (saturation < 30) & (brightness < 120)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. SAFETY ZONES (Protect Black Hair/Pants)
    # Hair: Top Center
    head_x0, head_x1 = int(w*0.4), int(w*0.6)
    head_y0, head_y1 = int(h*0.1), int(h*0.3)
    
    head_mask = np.zeros_like(alpha, dtype=bool)
    head_mask[head_y0:head_y1, head_x0:head_x1] = True
    
    # Legs: Bottom Center (Might be dark armor)
    legs_x0, legs_x1 = int(w*0.3), int(w*0.7)
    legs_y0, legs_y1 = int(h*0.6), int(h*0.95)
    legs_mask = np.zeros_like(alpha, dtype=bool)
    legs_mask[legs_y0:legs_y1, legs_x0:legs_x1] = True
    
    # Restore Alpha in Safety Zones IF pixels are Dark (not just noise)
    # We restoration logic: If it was removed by filter, put it back?
    # Only if it's REALLY dark (Black hair), not Grey background.
    # Hair is usually < 50 brightness. Background might be 50-100.
    # So: If brightness < 60 inside safety zone -> Keep it.
    
    should_save = (head_mask | legs_mask) & (brightness < 60)
    alpha[should_save] = 255
    
    # 4. POLISH
    # 1px Shave to kill borders
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Clean Artifacts (Corners)
    corner = 20
    alpha[0:corner, 0:corner] = 0
    alpha[0:corner, -corner:] = 0
    alpha[-corner:, 0:corner] = 0
    alpha[-corner:, -corner:] = 0

    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V303 Fire Polish Complete: {output_path}")

surgical_v303_fire_polish("public/assets/overlord_absolute_final.png")
