
import cv2
import numpy as np

def fix_earth_sky_holes():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Removing Blue/White sky holes from Upper Half of {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Define ROI: Upper 60% of image (Canopy Area)
    # We leave bottom 40% (Crystals/Roots) alone to prevent damage
    split_y = int(h * 0.6)
    
    upper_img = img[0:split_y, 0:w]
    
    # Safe Zone (Eyes)
    # Relative to Upper Image
    eye_y = int(h * 0.4) 
    safe_radius = int(w * 0.15)
    
    safe_mask = np.zeros((split_y, w), dtype=np.uint8)
    cv2.circle(safe_mask, (cx, eye_y), safe_radius, 255, -1)
    
    # Filter Condition: Blue > Red
    # This catches Blue Sky, Cyan, White (B=R), Gray (B=R).
    # Gold (R>B), Green (G>B, usually R>B or R~B), Brown (R>B) are safe.
    # Exception: Leaf Highlights might be White (B=R).
    # But Leaves are Green Dominant.
    # Let's verify: Green (50, 200, 50). B=50, R=50. B !> R. Safe.
    # White Highlight (200, 255, 200). B=200, R=200. B !> R? (Equal).
    # Condition: B >= R.
    
    b, g, r, a = cv2.split(upper_img)
    
    # Mask: B >= R
    # And Bright enough to be sky? > 100?
    bad_mask = (b >= r) & (b > 100)
    # Convert boolean to uint8
    bad_mask = bad_mask.astype(np.uint8) * 255
    
    # Exclude Safe Zone
    final_removal = cv2.bitwise_and(bad_mask, cv2.bitwise_not(safe_mask))
    
    # Apply Alpha 0 to Upper ROI
    upper_alpha = upper_img[:, :, 3]
    upper_alpha[final_removal > 0] = 0
    upper_img[:, :, 3] = upper_alpha
    
    # Merge back
    img[0:split_y, 0:w] = upper_img
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Sky Hole Removal)")

fix_earth_sky_holes()
