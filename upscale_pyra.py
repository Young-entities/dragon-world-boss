
import cv2
import numpy as np
import os

def upscale_unit(filepath, target_w=1200, target_h=896, fill_ratio=0.92):
    print(f"Upscaling unit content in {filepath}...")
    img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("File not found.")
        return

    # 1. Find bounding box of content
    alpha = img[:, :, 3]
    coords = cv2.findNonZero(alpha)
    if coords is None:
        print("Empty image.")
        return
        
    x, y, w, h = cv2.boundingRect(coords)
    content = img[y:y+h, x:x+w]
    
    # 2. Calculate best scale to fit fill_ratio of target
    scale_w = (target_w * fill_ratio) / w
    scale_h = (target_h * fill_ratio) / h
    scale = min(scale_w, scale_h)
    
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    resized_content = cv2.resize(content, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # 3. Create target canvas and center
    canvas = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    
    start_x = (target_w - new_w) // 2
    start_y = (target_h - new_h) // 2
    
    canvas[start_y:start_y+new_h, start_x:start_x+new_w] = resized_content
    
    cv2.imwrite(filepath, canvas)
    print(f"  Unit upscaled and centered on {target_w}x{target_h} canvas.")

# Apply specifically to Pyra
upscale_unit("public/assets/fire_empress_unit.png")
