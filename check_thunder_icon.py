
import cv2
import os

def check_icons():
    files = ["public/assets/element_thunder.png", "public/assets/element_electric.png"]
    for f in files:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            h, w = img.shape[:2]
            print(f"{f}: {w}x{h}")
        else:
            print(f"{f}: Not Found")

check_icons()
