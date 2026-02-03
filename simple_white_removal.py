
import cv2
import numpy as np

def simple_white_removal():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Simple White Removal from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    # Condition: Bright White
    # R>220, G>220, B>220
    b, g, r, a = cv2.split(img)
    
    mask_white = (r > 220) & (g > 220) & (b > 220)
    
    # Apply Alpha 0
    img[mask_white, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Simple White Removal)")

simple_white_removal()
