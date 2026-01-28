import cv2
import numpy as np
import os

def surgical_v403_palace_v2(input_path, output_path):
    print(f"Processing Palace V2 Unit: {input_path}")
    input_path = input_path.replace("\\", "/")
    img = cv2.imread(input_path)
    if img is None: return

    b, g, r = cv2.split(img)
    
    # GREEN EXTRACTION
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # DESPILL
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb)
    
    # POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, new_g, r, alpha])
    final_img[alpha == 0] = 0
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V403 Palace V2 Complete: {output_path}")

input_file = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_palace_v2_1769482840214.png"
output_file = "public/assets/crystal_fortress_unit.png"

surgical_v403_palace_v2(input_file, output_file)
