import cv2
import numpy as np

def surgical_v14_final_master(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # 1. FACIAL RECONSTRUCTION (Surgical)
    fx, fy = 163, 62
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove Mouth & Add defined nose
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    nose_color = (np.array(skin_color) * 0.65).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 4), (fx + 1, fy + 6), nose_color, -1)

    # 2. DUAL-PASS TRANSPARENCY
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # FIRST PASS: Floodfill (Outer Background)
    mask = np.zeros((h+2, w+2), np.uint8)
    temp_img = img.copy()
    fill_color = (255, 0, 255) # Magenta
    # Fill from all corners and some edge points to be thorough
    cv2.floodFill(temp_img, mask, (0,0), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(temp_img, mask, (w-1, 0), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(temp_img, mask, (w-1, h-1), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(temp_img, mask, (0, h-1), fill_color, (15,15,15), (15,15,15))
    
    # SECOND PASS: Aggressive targeted eraser (Inner Gaps)
    # We target the grey/white checkers specifically
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Checkers are Low Saturation (<40) and High Brightness (>180)
    inner_bg_mask = (s < 45) & (v > 185)
    
    # PROTECTION: We protect the core face and body skin from the second pass
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (145, 30), (185, 200), 255, -1)
    
    # Combine Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Rule 1: Outer connected background is transparent
    alpha[(temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)] = 0
    # Rule 2: Inner checkerboard pixels are transparent (if not protected)
    alpha[inner_bg_mask & (protection == 0)] = 0
    # Rule 3: Forced protection
    alpha[protection == 255] = 255

    # 3. SPRITE POLISH
    rgba[:,:,3] = alpha
    # Remove outer black/grey frame borders
    rgba = rgba[8:h-12, 10:w-10]
    nh, nw = rgba.shape[:2]
    
    # HD Reconstruction (4x)
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Masterpiece Finalized: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v14_final_master(source, "public/assets/water_deity_unit_final.png")
