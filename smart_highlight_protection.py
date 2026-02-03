
import cv2
import numpy as np

def smart_highlight_protection():
    # Source: The generated image with White Background (Artifact 8280) we are restoring from
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_white_bg_1769803384079.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Smart Highlight Protection processing from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    # 1. GrabCut for Outer Background removal
    mask = np.zeros(img.shape[:2], np.uint8)
    h, w = img.shape[:2]
    rect = (5, 5, w-10, h-10)
    
    # Init with Rect
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # Add Alpha 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask2 * 255
    
    # 2. Internal Hole Removal using Morphological Filtering
    # This separates "Big Sky Blobs" from "Small Detail Highlights"
    
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    
    # Bright Areas (> 180)
    bright_mask = (v > 180).astype(np.uint8) * 255
    
    # Morphological Opening
    # Kernel size 5x5: Removes features smaller than 5px (Highlights)
    kernel = np.ones((5,5), np.uint8)
    opened_mask = cv2.morphologyEx(bright_mask, cv2.MORPH_OPEN, kernel)
    
    # Opened Mask contains Big Bright Blobs.
    # We want to remove these.
    
    # Safe Zones: Eyes (Center) - They are big and bright!
    cx, cy = w // 2, h // 2
    eye_y = int(h * 0.38) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Final Removal Mask = Opened Mask AND NOT Safe Zone
    to_remove = cv2.bitwise_and(opened_mask, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0
    img[to_remove > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Smart Morphological Filter)")

smart_highlight_protection()
