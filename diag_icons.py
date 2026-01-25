import cv2
import numpy as np
import os

def check_icons():
    files = ['public/assets/element_fire_v4.png', 'public/assets/element_water.png']
    for p in files:
        if not os.path.exists(p):
            print(f"Missing: {p}")
            continue
        img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        a = img[:,:,3]
        nz = np.nonzero(a)
        y_min, y_max = nz[0].min(), nz[0].max()
        x_min, x_max = nz[1].min(), nz[1].max()
        vis_h = y_max - y_min
        vis_w = x_max - x_min
        print(f"FILE: {p}")
        print(f"  Canvas: {h}x{w}")
        print(f"  Visible Content: {vis_h}x{vis_w} (Bounds: y={y_min}-{y_max}, x={x_min}-{x_max})")
        print(f"  Vertical Offset (from center): {((y_min + y_max)/2) - (h/2)}")
        print("-" * 30)

if __name__ == "__main__":
    check_icons()
