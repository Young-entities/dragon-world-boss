
import cv2
import os

def check_new_dims():
    files = [
        "public/assets/earth_icon.png",
        "public/assets/earth_minion_final.png",
        "public/assets/earth_tree_bg_final.png",
        "public/assets/overlord_face_crop.png",
        "public/assets/overlord_absolute_final.png",
        "public/assets/electric_bg_final.png"
    ]
    
    for f in files:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            if img is not None:
                h, w = img.shape[:2]
                print(f"{f}: {w}x{h} (Aspect: {w/h:.2f})")
            else:
                print(f"{f}: Failed to load")
        else:
            print(f"{f}: Not found")

check_new_dims()
