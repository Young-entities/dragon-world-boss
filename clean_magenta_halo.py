
import cv2
import numpy as np

def clean_magenta_halo():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Cleaning Magenta Halo from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
    
    # 1. Erode Alpha to shave off the edge
    # This removes the 1px wide magenta fringe
    alpha = img[:, :, 3]
    kernel = np.ones((3,3), np.uint8) # 3x3 erodes ~1px radius
    eroded_alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # 2. Despill: Check borders for Magenta tint
    # If pixel is significantly Magenta-ish, kill it or Desaturate it?
    # R > G + 20 AND B > G + 20
    b, g, r, a = cv2.split(img)
    magenta_tint = (r > g + 20) & (b > g + 20) & (a > 0)
    
    # Turn Magenta Tints Transparent (Aggressive cleanup)
    # Applying this to the eroded image
    
    final_alpha = eroded_alpha.copy()
    final_alpha[magenta_tint] = 0
    
    img[:, :, 3] = final_alpha
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Halo Removal)")

clean_magenta_halo()
