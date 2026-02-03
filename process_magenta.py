
import cv2
import numpy as np

def process_magenta():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_magenta_bg_1769842106820.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Processing Earth Unit (Magenta Key) from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Magenta Key
    # R>200, B>200, G<150
    # Perfect Magenta is 255, 0, 255.
    
    b, g, r, a = cv2.split(img)
    
    mask_magenta = (r > 200) & (b > 200) & (g < 150)
    
    img[mask_magenta, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Magenta Chroma Key)")

process_magenta()
