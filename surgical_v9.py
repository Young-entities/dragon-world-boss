import cv2
import numpy as np

def surgical_v9_conservative(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # 0. DO NOT CROP YET. Let's see everything.
    h, w = img.shape[:2]

    # 1. Face Coordinates (Manual Identification on 324x211)
    # The character is roughly in the center of the 324px width.
    # Center = 162.
    face_x = 163
    face_y = 60
    
    # Remove mouth
    skin_roi = img[face_y-10:face_y-5, face_x-5:face_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    cv2.circle(img, (face_x, face_y + 11), 1, skin_color, -1)
    
    # Add Nose
    nose_color = (np.array(skin_color) * 0.65).astype(np.uint8).tolist()
    cv2.circle(img, (face_x, face_y + 4), 1, nose_color, -1)

    # 2. Advanced Transparency (Nuclear Option)
    # The checkers are the enemy.
    # Checkers are: White [255, 255, 255] and Light Grey [239, 239, 239]
    # We will specifically target these exact colors.
    
    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Create mask for White and Light Grey
    # White
    mask_white = (img[:,:,0] > 250) & (img[:,:,1] > 250) & (img[:,:,2] > 250)
    # Light Grey (Approx 239)
    mask_grey = (img[:,:,0] > 230) & (img[:,:,1] > 230) & (img[:,:,2] > 230) & (img[:,:,0] < 245)
    
    # Set Alpha to 0 for these
    rgba[mask_white, 3] = 0
    rgba[mask_grey, 3] = 0
    
    # Protect Face
    # Solid block around face
    rgba[face_y-20:face_y+20, face_x-15:face_x+15, 3] = 255

    # 3. Upscale (2x for clarity)
    result = cv2.resize(rgba, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
    
    cv2.imwrite(output_path, result)
    print(f"Surgical V9 Conservative completed: {output_path}")

surgical_v9_conservative("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
