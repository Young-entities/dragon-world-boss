
import cv2
import numpy as np

def final_hole_punch():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Super Aggressive Hole Punch from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Analyze HSV
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    s = hsv[:, :, 1]
    
    # Aggressive Filter
    # V > 130 (Catches even dark gray/dirty white)
    # S < 140 (Catches anything less than 55% saturated)
    # Gold (S=255) and Green Leaves (S~190) should be Safe.
    # Eyes (S~50) will be Hit -> Need Protection.
    bad_mask = (v > 130) & (s < 140)
    bad_mask = bad_mask.astype(np.uint8) * 255
    
    # Safe Zone (Eyes)
    # Center Circular Region
    eye_y = int(h * 0.38) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Apply Filter (Bad Pixels AND NOT Safe Zone)
    final_removal = cv2.bitwise_and(bad_mask, cv2.bitwise_not(safe_mask))
    
    # Update Alpha
    img[final_removal > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Final Hole Punch)")

final_hole_punch()
