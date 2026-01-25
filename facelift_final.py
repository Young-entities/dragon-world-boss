import cv2
import numpy as np

def surgical_facelift_v2(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Target Face Center
    fx, fy = 163, 62
    
    # 1. FACIAL RECONSTRUCTION
    # Sample skin tone
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # RE-PAINT FACE AREAS THAT WERE HOLLOW
    # We create a solid fill for the face region
    face_pts = np.array([[153, 40], [173, 40], [176, 75], [163, 85], [150, 75]], np.int32)
    cv2.fillPoly(img, [face_pts], skin_color)
    
    # 2. ADD NOSE (Pronounced shadow)
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 4), (fx + 1, fy + 5), nose_color, -1)

    # 3. TRANSPARENCY
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bg_mask = (hsv[:,:,1] < 50) & (hsv[:,:,2] > 180)
    
    # Protection Mask
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(protection, [face_pts], 255)
    cv2.rectangle(protection, (100, 85), (230, 195), 255, -1) # Body protection
    
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask & (protection == 0)] = 0
    alpha[protection == 255] = 255 # Hard force protection
    
    # Blue protection
    blue_m = cv2.inRange(hsv, np.array([90, 40, 40]), np.array([150, 255, 255]))
    alpha[blue_m == 255] = 255

    # 4. Upscale & Save
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    final = cv2.resize(rgba, (nw * 4, nh * 4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Facelift complete: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_facelift_v2(source, "public/assets/water_deity_unit_final.png")
