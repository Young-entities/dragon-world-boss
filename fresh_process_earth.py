
import cv2
import numpy as np

def fresh_process_earth():
    # Source: The generated image with White Background (Artifact 8280)
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_white_bg_1769803384079.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Fresh start processing from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    # 1. GrabCut for Outer Background
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    h, w = img.shape[:2]
    # Rect covers practically whole image, let GrabCut find the object
    rect = (5, 5, w-10, h-10)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # Add Alpha 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask2 * 255
    
    # 2. Internal Hole Removal (Targeting White/Gray/Pale Yellow/Cyan)
    # Define Safe Zone (Eyes)
    cx, cy = w // 2, h // 2
    eye_y = int(h * 0.38) # Slightly higher
    safe_radius = int(w * 0.12)
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Define Region of Interest for aggressive cleaning: Upper Canopy Area
    # Exclude Crystals (Bottom) and Spires (Mid-Lower Right)
    # y range: 0 to 0.6*h
    
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    s = hsv[:, :, 1]
    
    # Target: Bright (V>180) AND Low-Med Saturation (S<90)
    # This catches White, Gray, Pale Yellow.
    # Leaves are High Sat.
    bad_color_mask = (v > 180) & (s < 90)
    bad_color_mask = bad_color_mask.astype(np.uint8) * 255
    
    # Target: Cyan/Blue (H roughly 80-130 in OpenCV scale? Half of 360)
    # Or just B > R + 20
    b, g, r, a = cv2.split(img)
    blue_mask = (b > r + 20).astype(np.uint8) * 255
    
    combined_bad = cv2.bitwise_or(bad_color_mask, blue_mask)
    
    # Restrict to Upper Region (y < 0.6h) to save crystals/roots
    region_mask = np.zeros((h, w), dtype=np.uint8)
    region_mask[0:int(h*0.6), :] = 255
    
    final_removal = cv2.bitwise_and(combined_bad, region_mask)
    
    # Exclude Safe Zone (Eyes)
    final_removal = cv2.bitwise_and(final_removal, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0
    img[final_removal > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Fresh Process)")

fresh_process_earth()
