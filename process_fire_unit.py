import cv2
import numpy as np

def process_fire(unit_path, bg_path, output_unit_path, output_bg_path):
    # 1. PROCESS UNIT
    img = cv2.imread(unit_path)
    if img is None:
        print("Unit load failed")
        return

    # Chroma Key (Green)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Green is around 60.
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    bg_mask = cv2.inRange(hsv, lower_green, upper_green)
    fg_mask = cv2.bitwise_not(bg_mask)
    
    # Despill (Remove Green fringe)
    b, g, r = cv2.split(img)
    avg_rb = (r.astype(np.int16) + b.astype(np.int16)) // 2
    spill = (g > r) & (g > b)
    np.putmask(g, spill, avg_rb.astype(np.uint8))
    
    # Erode smooth
    kernel = np.ones((3,3), np.uint8)
    fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
    
    rgba = cv2.merge([b, g, r, fg_mask])
    
    # CROP Transparency
    coords = cv2.findNonZero(fg_mask)
    if coords is not None:
        x, y, w_box, h_box = cv2.boundingRect(coords)
        cropped = rgba[y:y+h_box, x:x+w_box]
    else:
        cropped = rgba

    # RESIZE TO FIT LANDSCAPE (900x600)
    target_w = 900
    target_h = 600
    
    h_c, w_c = cropped.shape[:2]
    
    # Standard Fit (Contain 95%)
    # Since this is a "New Unit" and User likes BIG...
    # I'll try 98%
    max_h = int(target_h * 0.98)
    max_w = int(target_w * 0.98)
    
    scale = min(max_w/w_c, max_h/h_c)
    
    new_w = int(w_c * scale)
    new_h = int(h_c * scale)
    
    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    unit_canvas = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    # Center
    sx = (target_w - new_w) // 2
    sy = (target_h - new_h) // 2
    unit_canvas[sy:sy+new_h, sx:sx+new_w] = resized
    
    cv2.imwrite(output_unit_path, unit_canvas)
    print(f"Unit Saved: {output_unit_path}")

    # 2. PROCESS BG (If path provided)
    if bg_path:
        bg = cv2.imread(bg_path)
        if bg is not None:
            h_b, w_b = bg.shape[:2]
            target_ratio = target_w / target_h
            bg_ratio = w_b / h_b
            
            if bg_ratio > target_ratio:
                new_h_b = h_b
                new_w_b = int(h_b * target_ratio)
                cx = w_b // 2
                bg_cropped = bg[:, cx-new_w_b//2 : cx+new_w_b//2]
            else:
                new_w_b = w_b
                new_h_b = int(w_b / target_ratio)
                cy = h_b // 2
                bg_cropped = bg[cy-new_h_b//2 : cy+new_h_b//2, :]
                
            bg_final = cv2.resize(bg_cropped, (target_w, target_h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_bg_path, bg_final)
            print(f"BG Saved: {output_bg_path}")

process_fire(
    "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/fire_empress_fixed_eyes_1769712332922.png",
    "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/fire_empress_bg_1769712133569.png",
    "public/assets/fire_empress_unit.png",
    "public/assets/fire_empress_bg.png"
)
