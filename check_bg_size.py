
import cv2

def check_bg(path):
    img = cv2.imread(path)
    if img is None:
        print(f"{path}: Not Found")
        return
    h, w = img.shape[:2]
    print(f"{path}: {w}x{h}")

check_bg("public/assets/dark_void_bg.png")
check_bg("public/assets/celestial_bg.png")
