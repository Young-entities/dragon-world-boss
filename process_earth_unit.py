
import cv2
import numpy as np

def process_earth_unit():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_gen_v8_1769797235478.png"
    out = "public/assets/earth_minion.png"
    
    print(f"Processing Earth Unit from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        print("Source not found")
        return
        
    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Chroma Key Green Removal
    # Green is (0, 255, 0)
    # Range of Green
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    
    # Bright Green Range
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert mask (Background is Green, we want Foreground)
    fg_mask = cv2.bitwise_not(mask)
    
    # Apply Mask to Alpha
    img[:, :, 3] = fg_mask
    
    # Clean edges (Erode mask slightly to remove green fringe?)
    # Or just save. Chroma key usually leaves fringe.
    # Let's simple save for now.
    
    cv2.imwrite(out, img)
    print(f"Saved {out}")

process_earth_unit()
