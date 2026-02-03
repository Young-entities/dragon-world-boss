
import cv2
import numpy as np

def fix_internal_holes():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Removing internal background holes from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Safe Zone (Eyes)
    # Circle at center-ish
    # Eyes are typically near middle-top
    eye_y = int(h * 0.4) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Identify Background Colors to Remove
    # 1. White
    lower_white = np.array([220, 220, 220, 0])
    upper_white = np.array([255, 255, 255, 255])
    mask_white = cv2.inRange(img, lower_white, upper_white)
    
    # 2. Cyan/Blue Sky artifacts (if any)
    # R<200, G>200, B>200 (Bright Cyan)
    # Inspecting artifact: Left side has Cyan leaves?
    # User might think Cyan leaves are background.
    # But if I remove them, I remove leaves.
    # Safest is just remove WHITE/Near-White.
    
    # Combine Masks
    target_mask = mask_white
    
    # Exclude Safe Zone (Eyes)
    # We want to remove pixels where (TargetMask AND NOT SafeMask)
    final_removal_mask = cv2.bitwise_and(target_mask, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0
    img[final_removal_mask > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Internal Holes Removed)")

fix_internal_holes()
