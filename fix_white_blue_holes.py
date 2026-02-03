
import cv2
import numpy as np

def fix_white_blue_holes():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Aggressively removing White/Blue holes from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Safe Zone (Eyes)
    # Eyes are typically near middle-top
    eye_y = int(h * 0.4) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Condition 1: Bright White/Gray
    # R>200, G>200, B>200
    b, g, r, a = cv2.split(img)
    mask_white = cv2.inRange(img[:,:,:3], np.array([200, 200, 200]), np.array([255, 255, 255]))
    
    # Condition 2: Bright Cyan
    # B>200, G>180, R<200 (optional? White covers high R too)
    # Let's target Light Cyan specifically: High B, High G.
    mask_cyan = cv2.inRange(img[:,:,:3], np.array([200, 180, 0]), np.array([255, 255, 180])) # Low R allowed
    
    # Combine
    bad_pixels = cv2.bitwise_or(mask_white, mask_cyan)
    
    # Protect Safe Zone (Eyes)
    # Pixels to remove = Bad Pixels AND NOT Safe Zone
    pixels_to_remove = cv2.bitwise_and(bad_pixels, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0
    img[pixels_to_remove > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Aggressive Hole Punch)")

fix_white_blue_holes()
