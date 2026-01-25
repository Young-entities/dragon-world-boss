import cv2
import numpy as np

def surgical_v7_final(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # Original is small: 324x211
    h, w = img.shape[:2]

    # 1. Mouth Removal / Nose Addition
    # Coordinates in the 324x211 image:
    # Face center is roughly x=163, y=60
    face_x, face_y = 163, 62
    
    # Sample skin color (forehead)
    skin_roi = img[face_y-12:face_y-8, face_x-5:face_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove mouth
    cv2.circle(img, (face_x, face_y + 10), 2, skin_color, -1)
    
    # Add Nose
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    cv2.line(img, (face_x, face_y + 3), (face_x, face_y + 5), nose_color, 1)

    # 2. Advanced Background Removal
    # The checkers are the issue. We'll use a combination of HSV and Saturation.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Create an alpha mask
    # Rule: Background pixels are high value (v > 180) and low saturation (s < 50)
    # AND they shouldn't be in the core character area.
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    
    # Identify background (checkers) 
    bg_mask = (s < 60) & (v > 170)
    
    # Explicitly protect the character's skin/face
    # Face area: (150, 40) to (180, 80)
    face_protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(face_protection, (150, 40), (180, 85), 255, -1)
    
    # Apply transparency to bg, but NOT to protected areas
    alpha[bg_mask] = 0
    alpha[face_protection == 255] = 255
    
    # 3. Smoothing
    # Use a small bilateral filter or blur on alpha to clean edges
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # 4. Upscale (3x to make it look decent)
    img_hd = cv2.resize(img, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    alpha_hd = cv2.resize(alpha, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    
    # Merge
    b, g, r = cv2.split(img_hd)
    rgba = cv2.merge([b, g, r, alpha_hd])
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V7 Final completed: {output_path}")

surgical_v7_final("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
