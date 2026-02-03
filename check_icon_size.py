
import cv2

def check_icon(path):
    img = cv2.imread(path)
    if img is None:
        print(f"{path}: Not Found")
        return
    h, w = img.shape[:2]
    print(f"{path}: {w}x{h}")

check_icon("public/assets/dark_deity_icon.png")
