import cv2
import numpy as np

def make_portrait_assets():
    # 1. Background (Crop to 3:4) - Target 768x1024
    bg = cv2.imread("public/assets/dark_void_bg.png")
    if bg is not None:
        h, w = bg.shape[:2]
        # Target ratio 3:4 (0.75)
        # Current 1:1.
        # Crop width.
        new_w = int(h * 0.75)
        start_x = (w - new_w) // 2
        crop_bg = bg[:, start_x:start_x+new_w]
        cv2.imwrite("public/assets/dark_void_bg.png", crop_bg)
        print("Cropped Background to Portrait.")

    # 2. Unit (Pad to 3:4) - Target 3:4 Canvas
    # Current Unit is likely Square (or close to it)
    unit = cv2.imread("public/assets/dark_deity_unit.png", cv2.IMREAD_UNCHANGED)
    if unit is not None:
        h, w = unit.shape[:2]
        # If w > h, pad h. If h ~= w, pad h to meet 3:4.
        # Target H = W / 0.75 = W * 1.333
        target_h = int(w * 1.333)
        
        if target_h > h:
            pad_total = target_h - h
            pad_top = pad_total // 2
            pad_bot = pad_total - pad_top
            
            # Create new canvas
            new_canvas = np.zeros((target_h, w, 4), dtype=np.uint8)
            # Paste old center
            new_canvas[pad_top:pad_top+h, 0:w] = unit
            
            cv2.imwrite("public/assets/dark_deity_unit.png", new_canvas)
            print("Padded Unit to Portrait (3:4).")
        else:
            print("Unit is already portrait enough?")

make_portrait_assets()
