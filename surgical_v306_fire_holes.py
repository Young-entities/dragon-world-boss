import cv2
import numpy as np
import glob
import os

def surgical_v306_fire_holes(output_path):
    # 1. SOURCE
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    latest_file = files[0] if files else None
    if not latest_file: return
    print(f"Using Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # Run V305 FloodFill Logic First
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1)]
    loDiff = (10, 10, 10)
    upDiff = (10, 10, 10)
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    for seed in seeds:
        cv2.floodFill(img, mask, seed, (0,0,0), loDiff, upDiff, flood_flags)
    bg_mask = mask[1:h+1, 1:w+1]
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[bg_mask == 255] = 0
    
    # 2. HOLE PUNCH (The Fix)
    # FloodFill missed internal holes (closed loops).
    # We detect them by "White Color" + "Low Saturation".
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness_min = np.minimum(np.minimum(r, g), b) # Use min channel brightness to be strict?
    # Actually just check if all channels are bright.
    
    is_bright_white = (r > 230) & (g > 230) & (b > 230)
    is_low_sat = (saturation < 15)
    
    is_white_hole = is_bright_white & is_low_sat
    
    # 3. SAFETY ZONES
    # Protect Face (Eyes/Teeth might be White/LowSat)
    # Face is usually top center
    head_x0, head_x1 = int(w*0.4), int(w*0.6)
    head_y0, head_y1 = int(h*0.1), int(h*0.3)
    head_mask = np.zeros_like(alpha, dtype=bool)
    head_mask[head_y0:head_y1, head_x0:head_x1] = True
    
    # Apply Punch (Outside Face)
    # Only pixels that are currently opaque
    punch_mask = is_white_hole & (~head_mask) & (alpha == 255)
    alpha[punch_mask] = 0
    
    # 4. SIDEBAR CLEAN (V304 Logic)
    brightness_sum = r.astype(int) + g.astype(int) + b.astype(int)
    secure_zone_x = int(w * 0.85)
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    is_artifact = (brightness_sum < 100) 
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
    print(f"Surgical V306 Fire Holes Complete: {output_path}")

surgical_v306_fire_holes("public/assets/overlord_absolute_final.png")
