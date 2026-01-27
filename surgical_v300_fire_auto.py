import cv2
import numpy as np
import glob
import os

def surgical_v300_fire_auto(output_path):
    # 1. FIND SOURCE
    # Look for newest PNG in parent directory
    search_pattern = "../*.png"
    files = glob.glob(search_pattern)
    if not files: 
        print("No source files found!")
        return
    
    # Sort by time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Detected Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None: return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. DETECT BACKGROUND
    # Sample 4 corners (10x10)
    corners = []
    corners.append(img[0:10, 0:10])
    corners.append(img[0:10, w-10:w])
    corners.append(img[h-10:h, 0:10])
    corners.append(img[h-10:h, w-10:w])
    
    avg_color = np.mean([np.mean(c, axis=(0,1)) for c in corners], axis=0) # BGR
    print(f"Average Corner Color (BGR): {avg_color}")
    
    B, G, R = avg_color
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    
    # DECISION TREE
    if G > R + 40 and G > B + 40:
        print("Mode: GREEN SCREEN")
        # Green Extraction
        is_bg = (g.astype(int) > r.astype(int) + 20) & \
                (g.astype(int) > b.astype(int) + 20) & \
                (g > 50)
        alpha[is_bg] = 0
        
        # Despill
        max_rb = np.maximum(r, b)
        g = np.minimum(g, max_rb)
        
    elif B < 40 and G < 40 and R < 40:
        print("Mode: BLACK SCREEN")
        # Black Extraction
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        is_bg = brightness < 50
        alpha[is_bg] = 0
        
    elif B > 200 and G > 200 and R > 200:
        print("Mode: WHITE SCREEN")
        # White Extraction
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        is_bg = brightness > 700 # (230*3)
        alpha[is_bg] = 0
        
    else:
        print("Mode: UNKNOWN (Assuming Complex/Cropped). using Smart Seg?")
        # Fallback: Assume Black if darkish, White if brightish
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        if np.mean(brightness) < 300:
             is_bg = brightness < 50
             print("Fallback: Dark Extraction")
        else:
             is_bg = brightness > 700
             print("Fallback: Light Extraction")
        alpha[is_bg] = 0

    # 3. POLISH (Standard)
    # Shave 1px
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # 4. SAVE
    # Merge
    # Note: If Green Screen, we updated 'g'.
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V300 Fire Auto Complete: {output_path}")

# Target: Fire Unit (ID 2 Full Image)
surgical_v300_fire_auto("public/assets/overlord_absolute_final.png")
