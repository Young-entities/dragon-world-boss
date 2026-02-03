
import cv2
import os

def check_dims():
    files = [
        "public/assets/overlord_face_crop.png",
        "public/assets/overlord_absolute_final.png",
        "public/assets/water_deity_face_crop.png",
        "public/assets/water_deity_unit_final.png",
        "public/assets/water_deity_card_bg.png",
        "public/assets/electric_god_icon.png",
        "public/assets/electric_god_unit_clean.png",
        "public/assets/electric_bg_final.png",
        "public/assets/earth_minion.png",
        "public/assets/earth_tree_bg.png"
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

check_dims()
