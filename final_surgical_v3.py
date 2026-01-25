import cv2
import numpy as np

def final_surgical_v3(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return

    # 1. Mouth Removal - Intelligent Patching
    # Identify skin tones in the center-top area
    h, w = img.shape[:2]
    face_zone = img[int(h*0.2):int(h*0.4), int(w*0.4):int(w*0.6)]
    
    # Simple median skin color
    skin_color = np.median(face_zone.reshape(-1, 3), axis=0).astype(np.uint8)
    
    # Mouth position in the unit (relative to center)
    # y=58, x=163 roughly for this 324x211 image
    mouth_y, mouth_x = 59, 163
    
    # Patch mouth area
    cv2.circle(img, (mouth_x, mouth_y), 2, skin_color.tolist(), -1)
    
    # 2. Advanced Background Removal (Checkered pattern)
    # The checkers are white/light-grey. 
    # Unit is vibrant blue/black.
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Mask for light colors (background)
    lower_bg = np.array([0, 0, 220]) 
    upper_bg = np.array([180, 50, 255])
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # Character Mask
    char_mask = cv2.bitwise_not(bg_mask)
    
    # Clean up alpha
    kernel = np.ones((2,2), np.uint8)
    char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_OPEN, kernel)
    char_mask = cv2.GaussianBlur(char_mask, (3,3), 0)

    # 3. Save as large high-quality PNG (rescale if needed to match other units)
    # Current is 324x211. Let's upscale to 648x422 to maintain sharpness in UI
    img_rescaled = cv2.resize(img, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
    char_mask_rescaled = cv2.resize(char_mask, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
    
    b, g, r = cv2.split(img_rescaled)
    rgba = cv2.merge([b, g, r, char_mask_rescaled])
    
    cv2.imwrite(output_path, rgba)
    print(f"Final Surgical V3 completed: {output_path}")

final_surgical_v3("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769301101122.png", "public/assets/water_deity_unit_final.png")
