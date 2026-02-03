
import cv2
import numpy as np
import shutil

def process_holy(input_path, output_base, output_circle):
    print(f"Processing sharp holy icon from: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return
        
    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # Remove White Background (Floodfill corners)
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1)]
    lo = (20, 20, 20)
    up = (20, 20, 20) # Tolerance
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    flooder = img[:,:,:3].copy()
    for seed in seeds:
        cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
        
    bg_mask = mask[1:-1, 1:-1]
    img[bg_mask > 0, 3] = 0
    
    # Crop to Content
    a = img[:, :, 3]
    coords = cv2.findNonZero(a)
    if coords is None:
        return
    x, y, cw, ch = cv2.boundingRect(coords)
    content = img[y:y+ch, x:x+cw]
    
    # Normalize to Ratio 0.94 in 128x128 Canvas
    TARGET_CANVAS = 128
    TARGET_RATIO = 0.94
    
    target_content_size = int(TARGET_CANVAS * TARGET_RATIO) # ~120px
    
    # Resize Content to target_content_size
    # Use INTER_AREA for high quality shrinking (Assuming source > 120px)
    new_content = cv2.resize(content, (target_content_size, target_content_size), interpolation=cv2.INTER_AREA)
    
    # Place in Canvas
    new_img = np.zeros((TARGET_CANVAS, TARGET_CANVAS, 4), dtype=np.uint8)
    
    px = (TARGET_CANVAS - target_content_size) // 2
    py = (TARGET_CANVAS - target_content_size) // 2
    
    new_img[py:py+target_content_size, px:px+target_content_size] = new_content
    
    # Save both files
    cv2.imwrite(output_base, new_img)
    cv2.imwrite(output_circle, new_img)
    print(f"Saved sharp {output_base} and {output_circle}")

src = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_holy_sharp_vector_1769782205643.png"
out1 = "public/assets/element_holy.png"
out2 = "public/assets/element_holy_circle.png"

process_holy(src, out1, out2)
