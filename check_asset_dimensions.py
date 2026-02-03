
import cv2
import os

def check_dims():
    files = [
        "public/assets/earth_minion.png",
        "public/assets/earth_tree_bg.png",
        "public/assets/overlord_absolute_final.png",
        # Find another background if possible. 
        # monsters.js likely has "cardBackground" field?
        # I'll check monsters.js content again.
    ]
    
    for f in files:
        if os.path.exists(f):
            img = cv2.imread(f)
            if img is not None:
                h, w = img.shape[:2]
                print(f"{f}: {w}x{h} (Aspect: {w/h:.2f})")
            else:
                print(f"{f}: Failed to load")
        else:
            print(f"{f}: Not found")

check_dims()
