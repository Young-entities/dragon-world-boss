
import cv2
import numpy as np

def create_earth_icon():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_earth_vector_1769797432936.png"
    out_base = "public/assets/element_earth.png"
    out_circle = "public/assets/element_earth_circle.png"
    
    print(f"Creating Earth Icon (Ratio 0.94)...")
    
    img = cv2.imread(src)
    if img is None:
        return

    # BG Removal
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1)]
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    flooder = img[:,:,:3].copy()
    for seed in seeds:
        cv2.floodFill(flooder, mask, seed, (255,255,255), (15,15,15), (15,15,15), flags)
    img[mask[1:-1, 1:-1] > 0, 3] = 0
    
    # Crop
    a = img[:, :, 3]
    coords = cv2.findNonZero(a)
    x, y, cw, ch = cv2.boundingRect(coords)
    content = img[y:y+ch, x:x+cw]
    
    # Normalize 0.94
    # Save as 128px Canvas for safety
    TARGET_CANVAS = 128
    TARGET_RATIO = 0.94
    target_content_size = int(TARGET_CANVAS * TARGET_RATIO)
    
    new_content = cv2.resize(content, (target_content_size, target_content_size), interpolation=cv2.INTER_AREA)
    
    new_img = np.zeros((TARGET_CANVAS, TARGET_CANVAS, 4), dtype=np.uint8)
    px = (TARGET_CANVAS - target_content_size) // 2
    py = (TARGET_CANVAS - target_content_size) // 2
    
    new_img[py:py+target_content_size, px:px+target_content_size] = new_content
    
    cv2.imwrite(out_base, new_img)
    cv2.imwrite(out_circle, new_img)
    print(f"Saved {out_base} and {out_circle}")

create_earth_icon()
