
import cv2
import glob
import os
import numpy as np

def strict_normalize():
    print("Strictly standardizing all icons to Fire v4 ratio (0.815)...")
    
    # Target: Fire v4 (44 content / 54 canvas = 0.8148)
    TARGET_RATIO = 0.815
    
    files = [
        "public/assets/element_dark.png",
        "public/assets/element_holy.png",
        "public/assets/element_water.png",
        "public/assets/element_electric.png",
        "public/assets/element_fire_v4.png" # Include to verify/re-save consistent
    ]
    
    for f in files:
        if not os.path.exists(f):
            print(f"Skipping {f} (Not Found)")
            continue
            
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        
        # Get Content Dimensions
        if img.shape[2] == 4:
            a = img[:, :, 3]
            coords = cv2.findNonZero(a)
            if coords is not None:
                x, y, cw, ch = cv2.boundingRect(coords)
            else:
                print(f"Skipping {f} (Empty)")
                continue
        else:
            x, y, cw, ch = 0, 0, w, h
            
        content = img[y:y+ch, x:x+cw]
        
        # Calculate Perfect Canvas Size for this content
        max_content = max(cw, ch)
        target_canvas_size = int(max_content / TARGET_RATIO)
        
        # Ensure target_canvas_size is at least max_content + 2 (padding space)
        if target_canvas_size < max_content:
            target_canvas_size = max_content
            
        # Create New Canvas
        new_img = np.zeros((target_canvas_size, target_canvas_size, 4), dtype=np.uint8)
        
        # Center Content
        px = (target_canvas_size - cw) // 2
        py = (target_canvas_size - ch) // 2
        
        new_img[py:py+ch, px:px+cw] = content
        
        cv2.imwrite(f, new_img)
        print(f"Strictly Normalized {f}: Content {cw}x{ch} -> Canvas {target_canvas_size}x{target_canvas_size} (Ratio {max_content/target_canvas_size:.3f})")

strict_normalize()
