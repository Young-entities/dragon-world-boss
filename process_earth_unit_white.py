
import cv2
import numpy as np

def process_earth_white():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_white_bg_1769803384079.png"
    out = "public/assets/earth_minion.png"
    
    print(f"Processing Earth Unit (White BG) from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # FloodFill from Corners
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1)]
    
    # White Tolerance (15)
    # Background should be essentially white.
    # Unit (Green/Brown) is far from white.
    lo = (15, 15, 15)
    up = (15, 15, 15)
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    flooder = img[:,:,:3].copy()
    for seed in seeds:
        cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
        
    bg_mask = mask[1:-1, 1:-1]
    img[bg_mask > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (White Chroma Key)")

process_earth_white()
