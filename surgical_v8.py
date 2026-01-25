import cv2
import numpy as np

def surgical_v8_precise(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # 1. Surgical Crop - Remove the black frame and watermark tag
    # Original is (211, 324). 
    # Let's crop to remove about 8 pixels from all sides
    img = img[10:211-12, 12:324-12] 
    h, w = img.shape[:2]

    # 2. Face Processing
    # Center-ish: x = 162-12 = 150. y = 62-10 = 52.
    # Refined center: 151, 51
    face_x, face_y = 151, 51
    
    # Sample skin tone
    skin_roi = img[face_y-10:face_y-5, face_x-5:face_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove mouth
    cv2.circle(img, (face_x, face_y + 10), 1, skin_color, -1)
    # Add nose
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    cv2.circle(img, (face_x, face_y + 3), 1, nose_color, -1)

    # 3. Checkerboard Disintegration
    # Target the LIGHT GREY and WHITE checkers specifically
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Checkers are very low saturation (< 30) and very high brightness (> 210)
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    bg_mask = (s < 45) & (v > 190)
    
    # PROTECT the face and core unit area
    # Create a protection mask for the central character (x: 130-180)
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (130, 30), (180, 100), 255, -1) # Head/Face
    cv2.rectangle(protection, (120, 100), (200, 180), 255, -1) # Body
    
    # Apply transparency where it's BG and NOT protected
    alpha[bg_mask] = 0
    alpha[protection == 255] = 255
    
    # Special: Water dragons are blue. Protect blue pixels (H: 100-140)
    blue_mask = (hsv[:,:,0] > 90) & (hsv[:,:,0] < 150) & (s > 20)
    alpha[blue_mask] = 255

    # 4. Smoothing
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # 5. Upscale to HD (3x)
    img_hd = cv2.resize(img, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    alpha_hd = cv2.resize(alpha, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    
    b, g, r = cv2.split(img_hd)
    rgba = cv2.merge([b, g, r, alpha_hd])
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V8 Precise completed: {output_path}")

surgical_v8_precise("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
