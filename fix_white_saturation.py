
import cv2
import numpy as np

def fix_white_saturation():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Removing low-saturation bright areas (white/gray) from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Safe Zone (Eyes)
    eye_y = int(h * 0.4) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Analyze HSV
    # Convert BGR of the image to HSV (ignore alpha for conversion)
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    
    # Target: High Value (Bright) AND Low Saturation (White/Gray)
    # V > 180
    # S < 50 (0-255 scale)
    lower_target = np.array([0, 0, 180])
    upper_target = np.array([180, 50, 255])
    
    target_mask = cv2.inRange(hsv, lower_target, upper_target)
    
    # Remove Safe Zone pixels from target
    final_removal = cv2.bitwise_and(target_mask, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0
    img[final_removal > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Saturation Filter)")

fix_white_saturation()
