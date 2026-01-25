import cv2
import numpy as np

def surgical_v15_emergency_fix(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # 1. FACIAL RECONSTRUCTION (Surgical)
    # Target center for the face in the 324x211 source
    # We'll use a larger target just to be sure.
    fx, fy = 163, 62
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove Mouth & Add Nose
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    nose_color = (np.array(skin_color) * 0.6).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 3), (fx + 1, fy + 5), nose_color, -1)

    # 2. EMERGENCY PROTECTION
    # We protect the entire central vertical half of the image from any transparency.
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (w//4, 0), (3*w//4, h), 255, -1)
    
    # 3. BACKGROUND ERASE (Outer only)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Checkers mask
    bg_mask = (s < 50) & (v > 180)
    
    # Final Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Only erase if it's BG AND NOT PROTECTED
    alpha[bg_mask & (protection == 0)] = 0
    
    # HARD FORCE: No pixel in the center can be transparent
    alpha[protection == 255] = 255

    # 4. Save
    rgba[:,:,3] = alpha
    # Remove borders
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    final = cv2.resize(rgba, (nw * 4, nh * 4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Emergency Solidified: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v15_emergency_fix(source, "public/assets/water_deity_unit_final.png")
