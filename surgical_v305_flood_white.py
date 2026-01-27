import cv2
import numpy as np
import glob
import os

def surgical_v305_flood_white(output_path):
    # 1. SOURCE
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    latest_file = files[0] if files else None
    
    if not latest_file: return 

    print(f"Using Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    # Add Alpha Channel
    b, g, r = cv2.split(img)
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    rgba = cv2.merge([b, g, r, alpha])
    
    h, w = img.shape[:2]
    
    # 2. FLOOD FILL EXTRACTION (The Fix for White Box)
    # The user screenshot shows a solid white box around the unit.
    # Simple brightness thresholding failed because White > Black threshold.
    # We use FloodFill from corners to identify the background.
    
    # Create mask (needs to be h+2, w+2 for floodFill)
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # FloodFill Seed Points (4 corners)
    seeds = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1)]
    
    # Tolerance for White Background
    # (2, 2, 2) allows slight noise
    loDiff = (10, 10, 10)
    upDiff = (10, 10, 10)
    
    # Execute FloodFill on Alpha Channel indirectly?
    # No, we floodFill the image and update a mask.
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    
    for seed in seeds:
        # Check if seed is actually bright?
        # If seed is black (sidebar), we don't want to use White tolerance.
        # Check pixel color
        seed_b = b[seed[1], seed[0]]
        seed_g = g[seed[1], seed[0]]
        seed_r = r[seed[1], seed[0]]
        
        # Determine tolerance based on seed color (White vs Black)
        # If seed is White (>200), use White logic.
        # If seed is Black (<50), use Black logic.
        
        cv2.floodFill(img, mask, seed, (0,0,0), loDiff, upDiff, flood_flags)
        
    # Apply Mask to Alpha
    # Mask is h+2, w+2. Crop it.
    bg_mask = mask[1:h+1, 1:w+1]
    
    # Where mask is 255, it's Background -> Alpha 0
    alpha[bg_mask == 255] = 0
    
    # 3. SAFETY & CLEANUP
    # Keep the Head/Legs protection similar to V303?
    # FloodFill protects internal pixels automatically (unless holes exist).
    # If the White Background leaks into White Eyes... unlikely.
    # But usually FloodFill is safe.
    
    # 4. SIDEBAR CLEAN (V304 Logic)
    # There might still be a black bar the floodfill missed (if it wasn't connected to corners?)
    # Or if corners were white and bar is black.
    # Let's re-run the V304 "Kill Dark Artifacts on Right" logic.
    
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    secure_zone_x = int(w * 0.85)
    is_far_right = np.zeros_like(alpha, dtype=bool)
    is_far_right[:, secure_zone_x:] = True
    
    is_artifact = (brightness < 100) 
    alpha[is_artifact & is_far_right] = 0
    
    # 5. POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V305 Flood White Complete: {output_path}")

surgical_v305_flood_white("public/assets/overlord_absolute_final.png")
