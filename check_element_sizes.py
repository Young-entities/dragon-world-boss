
import cv2
import os
import glob

def check_sizes():
    # List all element_*.png files
    files = glob.glob("public/assets/element_*.png")
    
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        
        # Check content bbox
        content_w, content_h = 0, 0
        if img.shape[2] == 4:
            a = img[:, :, 3]
            coords = cv2.findNonZero(a)
            if coords is not None:
                x, y, cw, ch = cv2.boundingRect(coords)
                content_w, content_h = cw, ch
        
        print(f"{os.path.basename(f)}: Canvas {w}x{h}, Content {content_w}x{content_h}")

check_sizes()
