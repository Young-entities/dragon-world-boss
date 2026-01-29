import cv2
import numpy as np

def normalize_dark(source_path, output_path):
    img = cv2.imread(source_path) # BGR
    if img is None:
        print("Source not found")
        return

    # 1. Chroma Key (Neon Green)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    bg_mask = cv2.inRange(hsv, lower_green, upper_green)
    fg_mask = cv2.bitwise_not(bg_mask)
    
    # 2. Despill / Purify
    b, g, r = cv2.split(img)
    avg_rb = (r.astype(np.int16) + b.astype(np.int16)) // 2
    spill = (g > r) & (g > b)
    np.putmask(g, spill, avg_rb.astype(np.uint8))
    
    kernel = np.ones((3,3), np.uint8)
    fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
    
    rgba = cv2.merge([b, g, r, fg_mask])
    
    # 3. Auto-Crop Transparency
    coords = cv2.findNonZero(fg_mask)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = rgba[y:y+h, x:x+w]
    
    # Get dimensions of clean crop
    h_c, w_c = cropped.shape[:2]

    # ZOOM CROP (1.05x)
    # Very subtle zoom (5%)
    # Pushes limits without "nuking" details
    zoom_factor = 1.05
    center_y, center_x = h_c // 2, w_c // 2
    crop_h = int(h_c / zoom_factor)
    crop_w = int(w_c / zoom_factor)
    
    y1 = max(0, center_y - crop_h // 2)
    y2 = min(h_c, center_y + crop_h // 2)
    x1 = max(0, center_x - crop_w // 2)
    x2 = min(w_c, center_x + crop_w // 2)
    
    zoomed_crop = cropped[y1:y2, x1:x2]
    h_z, w_z = zoomed_crop.shape[:2]

    # 5. Fit to Landscape Canvas (900x600)
    target_w = 900
    target_h = 600
    
    # Fit Height (100% - No padding)
    max_h = int(target_h * 1.0)
    max_w = int(target_w * 1.0)
    
    scale = min(max_w/w_z, max_h/h_z)
    
    new_w = int(w_z * scale)
    new_h = int(h_z * scale)
    
    resized = cv2.resize(zoomed_crop, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Place on Canvas
    canvas = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    start_x = (target_w - new_w) // 2
    start_y = (target_h - new_h) // 2
    
    canvas[start_y:start_y+new_h, start_x:start_x+new_w] = resized
    
    # OUTPUT V7
    output_path = output_path.replace(".png", "_v7.png")
    cv2.imwrite(output_path, canvas)
    print(f"Normalized Asset V7 Complete (Zoomed 1.05x): {output_path}")

normalize_dark("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_azaerth_greenscreen_regen_1769702009898.png", "public/assets/dark_deity_unit.png")
