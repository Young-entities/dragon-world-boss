
import cv2
import glob
import os
import numpy as np

def normalize_to_perfect_size():
    print("Normalizing ALL icons to match Fire Circle (Units Tab) Ratio ~0.94...")
    
    TARGET_RATIO = 0.94
    
    # List of elements
    elements = ["fire", "water", "electric", "dark", "holy", "earth", "wind"]
    
    # Generate/Process both Base and Circle variants
    for el in elements:
        # Define paths
        base_path = f"public/assets/element_{el}.png"
        circle_path = f"public/assets/element_{el}_circle.png"
        
        # Fire is special (v4 for base).
        if el == "fire":
             base_path = "public/assets/element_fire_v4.png"
             
        # Check if Base exists
        if not os.path.exists(base_path):
             # Try fallback naming just in case? No.
             if el == "earth" and os.path.exists("public/assets/element_earth.png"):
                 pass # check
             else:
                 if os.path.exists(f"public/assets/element_{el}.png"): # standard
                      base_path = f"public/assets/element_{el}.png"
                 else:
                      print(f"Skipping {el} (Base not found)")
                      continue

        # Process Base
        process_file(base_path, TARGET_RATIO)
        
        # Check if Circle exists. If not, create copy from Base
        if not os.path.exists(circle_path):
             print(f"Creating missing {circle_path} from Base...")
             import shutil
             shutil.copy2(base_path, circle_path)
             
        # Process Circle
        process_file(circle_path, TARGET_RATIO)

def process_file(f, target_ratio):
    img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    if img is None:
        return
        
    h, w = img.shape[:2]
    
    # Get Content
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
             x, y, cw, ch = cv2.boundingRect(coords)
        else:
             return
    else:
         x, y, cw, ch = 0, 0, w, h
         
    content = img[y:y+ch, x:x+cw]
    
    max_content = max(cw, ch)
    target_canvas = int(max_content / target_ratio)
    
    if target_canvas < max_content: target_canvas = max_content
    
    new_img = np.zeros((target_canvas, target_canvas, 4), dtype=np.uint8)
    px = (target_canvas - cw) // 2
    py = (target_canvas - ch) // 2
    
    new_img[py:py+ch, px:px+cw] = content
    
    cv2.imwrite(f, new_img)
    print(f"Updated {f} -> Ratio {target_ratio}")

normalize_to_perfect_size()
