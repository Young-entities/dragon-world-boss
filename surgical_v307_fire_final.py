import cv2
import numpy as np
import glob
import os

def surgical_v307_fire_final(output_path):
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
    
    # 2. AGGRESSIVE HOLE PUNCH (The Fix)
    # User showed a persistent greyish/tinted spot behind hair.
    # We relax thresholds specifically in the upper body area.
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness = r.astype(int) + g.astype(int) + b.astype(int) # Sum 0-765
    brightness_per_channel = brightness / 3.0
    
    # Standard Punch (V306): Bright > 230, Sat < 15
    is_standard_hole = (r > 230) & (g > 230) & (b > 230) & (saturation < 15)
    
    # Aggressive Punch: Bright > 180, Sat < 25
    # Only applies to upper body (hair area), excluding face.
    is_aggressive_hole = (brightness_per_channel > 180) & (saturation < 25)
    
    # 3. SAFETY ZONES
    head_x0, head_x1 = int(w*0.4), int(w*0.6)
    head_y0, head_y1 = int(h*0.1), int(h*0.3)
    head_mask = np.zeros_like(alpha, dtype=bool)
    head_mask[head_y0:head_y1, head_x0:head_x1] = True
    
    # Aggressive Zone: Upper Half
    upper_mask = np.zeros_like(alpha, dtype=bool)
    upper_mask[0:int(h*0.5), :] = True
    
    # Combine Logic
    # 1. Standard Hole check everywhere (except Head)
    # 2. Aggressive Hole check in Upper Half (except Head)
    
    punch_mask = (is_standard_hole & (~head_mask)) | (is_aggressive_hole & upper_mask & (~head_mask))
    
    # Only punch opaque pixels
    alpha[punch_mask & (alpha == 255)] = 0
    
    # 4. SIDEBAR CLEAN (V304 Logic)
    secure_zone_x = int(w * 0.85)
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    is_artifact = (brightness < 300) # Brightness Sum < 300 (avg < 100)
    alpha[is_artifact & is_far_right] = 0
    
    # 5. POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    corner = 20
    alpha[0:corner, 0:corner] = 0
    alpha[0:corner, -corner:] = 0
    alpha[-corner:, 0:corner] = 0
    alpha[-corner:, -corner:] = 0

    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V307 Fire Final Complete: {output_path}")

surgical_v307_fire_final("public/assets/overlord_absolute_final.png")
