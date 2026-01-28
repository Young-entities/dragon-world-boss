import cv2
import numpy as np
import os

def surgical_v405_palace_v4(input_path, output_path):
    print(f"Processing Palace V4 Unit: {input_path}")
    input_path = input_path.replace("\\", "/")
    img = cv2.imread(input_path)
    if img is None: return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # AUTO DETECT BACKGROUND
    is_green_dominant = (np.mean(g) > (np.mean(r) + 20)) and (np.mean(g) > (np.mean(b) + 20))
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    
    if is_green_dominant:
        print("Mode: GREEN SCREEN")
        is_bg = (g.astype(int) > r.astype(int) + 20) & \
                (g.astype(int) > b.astype(int) + 20) & \
                (g > 50)
        alpha[is_bg] = 0
        max_rb = np.maximum(r, b)
        g = np.minimum(g, max_rb)
    else:
        # Check White
        avg_corner = np.mean([img[0,0], img[0,w-1], img[h-1,0], img[h-1,w-1]], axis=0)
        B, G, R = avg_corner
        if B > 200 and G > 200 and R > 200:
            print("Mode: WHITE SCREEN (FloodFill)")
            mask = np.zeros((h+2, w+2), np.uint8)
            # FloodFill from Corners
            seeds = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1)]
            for seed in seeds:
                 cv2.floodFill(img, mask, seed, (0,0,0), (10,10,10), (10,10,10), 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
            bg_mask = mask[1:h+1, 1:w+1]
            alpha[bg_mask == 255] = 0
            
            # Additional White Hole Punch (similar to Fire Unit V306) if needed?
            # Let's start with FloodFill.
        else:
             print("Mode: UNKNOWN")
             # Fallback
    
    # POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V405 Palace V4 Complete: {output_path}")

input_file = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_palace_v4_1769483016335.png"
output_file = "public/assets/crystal_fortress_unit.png"

surgical_v405_palace_v4(input_file, output_file)
