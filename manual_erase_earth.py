
import cv2
import numpy as np

def manual_erase_earth():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Manually erasing persistent background blobs from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    h, w = img.shape[:2]
    
    # List of circles to erase: (x_ratio, y_ratio, radius_ratio)
    erasures = [
        (0.75, 0.38, 0.08),  # Right Top Hole
        (0.82, 0.45, 0.06),  # Right Lower Hole
        (0.20, 0.40, 0.08),  # Left Blue Patch
        (0.12, 0.35, 0.06),  # Left Far Edge
        (0.88, 0.35, 0.05),  # Right Far Edge
        (0.65, 0.30, 0.05),  # Top Center Right
        (0.35, 0.30, 0.05)   # Top Center Left
    ]
    
    # Create Erasure Mask
    erase_mask = np.zeros((h, w), dtype=np.uint8)
    
    for (rx, ry, rr) in erasures:
        cx = int(w * rx)
        cy = int(h * ry)
        rad = int(w * rr)
        # Draw white circle on mask
        cv2.circle(erase_mask, (cx, cy), rad, 255, -1)
    
    # Apply Blur to mask for soft edges?
    # Or hard eraser?
    # User said "still there", implies they want it GONE.
    # Hard erase is safer to ensure visibility.
    # But usually soft looks better.
    # I'll effectively subtract the mask from alpha.
    
    # Invert mask (We want to KEEP pixels where erase_mask is 0)
    keep_mask = cv2.bitwise_not(erase_mask)
    
    # Apply to Alpha
    current_alpha = img[:, :, 3]
    new_alpha = cv2.bitwise_and(current_alpha, keep_mask)
    img[:, :, 3] = new_alpha
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Manual Erasure)")

manual_erase_earth()
