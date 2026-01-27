import cv2
import numpy as np
import glob
import os

def surgical_v308_fire_perfect(output_path):
    # 1. SOURCE
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    latest_file = files[0] if files else None
    if not latest_file: return
    print(f"Using Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. FLOOD FILL + DILATION (The Fix for Outlines)
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1)]
    # Increase tolerance slightly to catch varying white shades
    loDiff = (15, 15, 15)
    upDiff = (15, 15, 15)
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    for seed in seeds:
        cv2.floodFill(img, mask, seed, (0,0,0), loDiff, upDiff, flood_flags)
    bg_mask = mask[1:h+1, 1:w+1]
    
    # DILATE THE BACKGROUND MASK
    # This expands the 'transparent' area into the 'solid' area.
    # Effectively eating the border outline left by FloodFill.
    kernel_dilate = np.ones((3,3), np.uint8)
    bg_mask = cv2.dilate(bg_mask, kernel_dilate, iterations=2) # 2-3px erosion of object
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[bg_mask == 255] = 0
    
    # 3. AGGRESSIVE HOLE PUNCH (V307 Logic)
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    brightness_per_channel = brightness / 3.0
    
    is_standard_hole = (r > 230) & (g > 230) & (b > 230) & (saturation < 15)
    is_aggressive_hole = (brightness_per_channel > 180) & (saturation < 25)
    
    head_x0, head_x1 = int(w*0.4), int(w*0.6)
    head_y0, head_y1 = int(h*0.1), int(h*0.3)
    head_mask = np.zeros_like(alpha, dtype=bool)
    head_mask[head_y0:head_y1, head_x0:head_x1] = True
    
    upper_mask = np.zeros_like(alpha, dtype=bool)
    upper_mask[0:int(h*0.5), :] = True
    
    punch_mask = (is_standard_hole & (~head_mask)) | (is_aggressive_hole & upper_mask & (~head_mask))
    alpha[punch_mask & (alpha == 255)] = 0
    
    # 4. SIDEBAR CLEAN (Moved further right)
    # The previous secure_zone_x = 0.85 might have cut the sword shadow.
    # The artifact bar is usually at the very edge.
    # Move to 0.95 (Last 5%)
    secure_zone_x = int(w * 0.95)
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    is_artifact = (brightness < 100)
    alpha[is_artifact & is_far_right] = 0
    
    # 5. POLISH
    # Final shave to ensure smoothness
    kernel_erode = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel_erode, iterations=1)
    
    corner = 20
    alpha[0:corner, 0:corner] = 0
    alpha[0:corner, -corner:] = 0
    alpha[-corner:, 0:corner] = 0
    alpha[-corner:, -corner:] = 0

    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V308 Fire Perfect Complete: {output_path}")

surgical_v308_fire_perfect("public/assets/overlord_absolute_final.png")
