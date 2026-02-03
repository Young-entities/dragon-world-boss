
import cv2
import numpy as np

def fix_earth_transparency():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_gen_v8_1769797235478.png"
    out = "public/assets/earth_minion.png"
    
    print(f"Fixing Earth Unit Transparency (Adaptive Tolerance)...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1)]
    
    # Tolerance 15 (Between 2 and 20)
    # Should catch noise but hopefully avoid leaves
    lo = (15, 15, 15)
    up = (15, 15, 15)
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    flooder = img[:,:,:3].copy()
    for seed in seeds:
        cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
        
    bg_mask = mask[1:-1, 1:-1]
    
    # Erode the mask (Expand the hole) ?? 
    # Wait, bg_mask is 255 where BG is found.
    # We want to Expand 255 region to eat into the fringe properly?
    # No, usually FloodFill eats enough if tolerance is good.
    # If we want to remove fringe, we Erode the OBJECT.
    # Object is (NOT bg_mask).
    # Let's simple apply alpha first.
    
    img[bg_mask > 0, 3] = 0
    
    # Optional: Remove Green Halo by Desaturating semi-transparent edges?
    # Too complex for now. Tolerance 15 + Floodfill should work if leaves are distinct.
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Tolerance 15)")

fix_earth_transparency()
