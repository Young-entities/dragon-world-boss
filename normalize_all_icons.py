
import cv2
import glob
import os
import numpy as np

def normalize_icons():
    files = glob.glob("public/assets/element_*.png")
    target_ratio = 0.82 # Content covers 82% of canvas (Matches Fire v4)
    
    # Exclude backup/version files if desired? 
    # Logic: Only process files that don't have _circle or versions if main exists?
    # User said "every single icon".
    # I'll process ALL 'element_*.png' found in the active usage list.
    # Active usage usually `element_fire_v4.png` (explicitly used) and `element_dark.png` etc.
    
    # Prioritize:
    key_files = [
        "public/assets/element_dark.png",
        "public/assets/element_holy.png",
        "public/assets/element_water.png",
        "public/assets/element_electric.png",
        "public/assets/element_earth.png",
        "public/assets/element_wind.png",
        "public/assets/element_fire_v4.png"
    ]
    
    for f in key_files:
        if not os.path.exists(f):
            continue
            
        print(f"Checking {f}...")
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        
        # Find Content
        if img.shape[2] == 4:
            a = img[:, :, 3]
            coords = cv2.findNonZero(a)
            if coords is not None:
                x, y, cw, ch = cv2.boundingRect(coords)
            else:
                continue # Empty
        else:
             # Assume full opaque
             cw, ch = w, h
             x, y = 0, 0
             
        # Check current ratio
        max_dim = max(cw, ch)
        current_canvas = max(w, h)
        ratio = max_dim / current_canvas
        
        print(f"  Ratio: {ratio:.2f}")
        
        # If ratio is too high (tight crop) -> Add Padding
        # Threshold: > 0.85
        if ratio > 0.85:
            print(f"  Standardizing {f} (adding padding)")
            
            # Target Canvas Size
            new_canvas_size = int(max_dim / target_ratio)
            
            # Create new square canvas
            new_img = np.zeros((new_canvas_size, new_canvas_size, 4), dtype=np.uint8)
            
            # Extract content
            content = img[y:y+ch, x:x+cw]
            
            # Paste center
            px = (new_canvas_size - cw) // 2
            py = (new_canvas_size - ch) // 2
            
            new_img[py:py+ch, px:px+cw] = content
            
            cv2.imwrite(f, new_img)
            print(f"  Saved updated {f}")
            
        # Also ensure aspect ratio of canvas is Square?
        elif abs(w - h) > 2: # Tolerance 2px
             print(f"  Squaring canvas for {f}")
             new_canvas_size = max(w, h)
             new_img = np.zeros((new_canvas_size, new_canvas_size, 4), dtype=np.uint8)
             
             px = (new_canvas_size - w) // 2
             py = (new_canvas_size - h) // 2
             
             new_img[py:py+h, px:px+w] = img
             cv2.imwrite(f, new_img)

normalize_icons()
