import cv2
import numpy as np

def surgical_v11_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # 0. High Quality Source (324x211)
    h, w = img.shape[:2]

    # 1. Face Coordinates (Corrected)
    # The character is in the center. x ~ 163.
    # Face y is around 62.
    fx, fy = 163, 62
    
    # Sample skin
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove mouth
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    
    # Add Nose
    nose_color = (np.array(skin_color) * 0.6).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 4), (fx + 1, fy + 5), nose_color, -1)

    # 2. Advanced Transparency (Dual Mask)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Checkers: Low Saturation (<45) and High Brightness (>180)
    bg_mask = (s < 45) & (v > 185)
    
    # PROTECTION MASK (Sacred Zone)
    # This block MUST remain solid.
    protection = np.zeros((h, w), dtype=np.uint8)
    # Face & Body Core: x from 145 to 185, y from 30 to 200
    cv2.rectangle(protection, (145, 30), (185, 200), 255, -1)
    
    # 3. Create Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask & (protection == 0)] = 0
    alpha[protection == 255] = 255 # Hard force protection
    
    # Protect blue water dragons (Hue 100-140)
    blue_p = (hsv[:,:,0] > 90) & (hsv[:,:,0] < 150) & (s > 25)
    alpha[blue_p] = 255

    # 4. Final Crop & Polish
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])
    # Remove the black frame borders (approx 10px off sides)
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    
    # 5. Perfect Upscale (4x)
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Brute force solidified: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v11_nuke(source, "public/assets/water_deity_unit_final.png")
