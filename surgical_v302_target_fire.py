import cv2
import numpy as np
import glob
import os

def surgical_v302_target_fire(output_path):
    # 1. TARGETED SOURCE
    # User confirmed this specific filename via screenshot
    target_pattern = "../Gemini_Generated_Image_40sf5z40sf5z40sf.png"
    files = glob.glob(target_pattern)
    
    if not files: 
        print(f"CRITICAL ERROR: File not found: {target_pattern}")
        # Try finding it in current dir?
        files = glob.glob(target_pattern.replace("../", ""))
        if not files:
            print("File essentially missing.")
            return

    latest_file = files[0]
    print(f"Using Targeted Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None: return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. DETECT BACKGROUND (Robustness)
    # Sample 4 corners (10x10)
    corners = []
    corners.append(img[0:10, 0:10])
    corners.append(img[0:10, w-10:w])
    corners.append(img[h-10:h, 0:10])
    corners.append(img[h-10:h, w-10:w])
    
    avg_color = np.mean([np.mean(c, axis=(0,1)) for c in corners], axis=0) # BGR
    B, G, R = avg_color
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    
    # DECISION TREE
    if G > R + 30 and G > B + 30: # Green Screen
        print("Mode: GREEN SCREEN")
        is_bg = (g.astype(int) > r.astype(int) + 20) & \
                (g.astype(int) > b.astype(int) + 20) & \
                (g > 50)
        alpha[is_bg] = 0
        max_rb = np.maximum(r, b)
        g = np.minimum(g, max_rb) # Despill
        
    elif B < 50 and G < 50 and R < 50: # Black Screen
        print("Mode: BLACK SCREEN")
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        is_bg = brightness < 50
        alpha[is_bg] = 0
        
    else: # Fallback (Complex) - Assume Black if average < 100
        print("Mode: UNKNOWN")
        brightness = r.astype(int) + g.astype(int) + b.astype(int)
        if np.mean(brightness) < 300: # < 100 avg per channel
             is_bg = brightness < 50
             print("Fallback: Dark Extraction")
        else:
             is_bg = brightness > 700
             print("Fallback: Light Extraction")
        alpha[is_bg] = 0

    # 3. POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # 4. SAVE
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V302 Targeted Fire Complete: {output_path}")

surgical_v302_target_fire("public/assets/overlord_absolute_final.png")
