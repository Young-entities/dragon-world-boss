
import cv2
import numpy as np
import shutil

def pad_icons_preserve_res():
    print("Padding Dark/Holy to exactly 0.94 ratio (matching Fire) while PRESERVING High Resolution...")
    
    files = ["public/assets/element_dark.png", "public/assets/element_holy.png"]
    TARGET_RATIO = 0.94
    
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        
        # Get Content
        if img.shape[2] == 4:
            a = img[:, :, 3]
            coords = cv2.findNonZero(a)
            if coords is not None:
                x, y, cw, ch = cv2.boundingRect(coords)
            else:
                 continue
        else:
             x, y, cw, ch = 0, 0, w, h
             
        content = img[y:y+ch, x:x+cw]
        
        # Calculate Target Canvas Size to achieve 0.94 Ratio
        max_content = max(cw, ch)
        target_canvas = int(max_content / TARGET_RATIO)
        
        # Ensure target_canvas matches High Res Needs
        # Do NO resizing of content. content is kept as is.
        # Just creating a larger canvas.
        
        new_img = np.zeros((target_canvas, target_canvas, 4), dtype=np.uint8)
        
        px = (target_canvas - cw) // 2
        py = (target_canvas - ch) // 2
        
        new_img[py:py+ch, px:px+cw] = content
        
        cv2.imwrite(f, new_img)
        print(f"Padded {f}: Content {cw}x{ch} -> Canvas {target_canvas}x{target_canvas} (Ratio {max_content/target_canvas:.3f})")
        
        # Update Circle Variant
        circle_path = f.replace(".png", "_circle.png")
        shutil.copy2(f, circle_path)
        print(f"Updated {circle_path}")

pad_icons_preserve_res()
