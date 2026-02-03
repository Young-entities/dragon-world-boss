
import cv2
import os

def check_holy():
    files = ["public/assets/element_holy.png", "public/assets/element_holy_circle.png"]
    for f in files:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            h, w = img.shape[:2]
            print(f"{f}: {w}x{h}")
        else:
            print(f"{f}: Not Found")

check_holy()
