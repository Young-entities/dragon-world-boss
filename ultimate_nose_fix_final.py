import cv2
import numpy as np

def ultimate_surgical_fixed_nose(input_path, output_path):
    # 1. Load the fresh image provided by the user
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image")
        return

    # 2. Perfect Crop - Removing all outside black frames and watermark tags
    # Source is (211, 324)
    # We crop specifically to capture the character and dragons fully
    img = img[8:211-12, 10:324-10] 
    h, w = img.shape[:2]

    # 3. Facial Reconstruction: The "Mystery Goddess" Look
    # Target center for THIS specific crop: x=151, y=50 roughly
    face_center_x, face_center_y = 151, 51
    
    # Sample skin-tone area (forehead/cheek)
    skin_roi = img[face_center_y-10:face_center_y-5, face_center_x-5:face_center_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # REMOVE MOUTH (Patching)
    # Patch area for mouth: x=151, y=59
    cv2.rectangle(img, (face_center_x - 5, face_center_y + 8), (face_center_x + 5, face_center_y + 11), skin_color, -1)
    
    # ADD DEFINED NOSE (The Big Request)
    # Anime noses typically have a small shadow dot or vertical line.
    # We want it clearly visible but elegant.
    nose_color = (np.array(skin_color) * 0.75).astype(np.uint8).tolist()
    # Distinct 2-pixel vertical nose tip
    cv2.line(img, (face_center_x, face_center_y + 3), (face_center_x, face_center_y + 5), nose_color, 1)

    # 4. Checkerboard Nuke + True Transparency
    # Target the high-brightness, low-saturation greys/whites of the checkers.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Mask background (Checkers/White)
    lower_bg = np.array([0, 0, 180]) 
    upper_bg = np.array([120, 50, 255])
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # Character Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask == 255] = 0
    
    # Restore character's vibrant blues (in case they were bright)
    # Target standard water hues
    blue_protection = cv2.inRange(hsv, np.array([90, 40, 40]), np.array([140, 255, 255]))
    alpha[blue_protection == 255] = 255

    # 5. Smooth blending
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # 6. HD RECONSTRUCTION (4x Lanczos Upscale)
    # This makes the small image look crisp and cinematic in the game.
    img_hd = cv2.resize(img, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
    mask_hd = cv2.resize(alpha, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
    
    b, g, r = cv2.split(img_hd)
    rgba = cv2.merge([b, g, r, mask_hd])
    
    # 7. Final Polish: Sharpen the nose area in HD
    # HD coordinates are 4x original
    nx_hd, ny_hd = face_center_x * 4, (face_center_y + 4) * 4
    cv2.circle(rgba, (nx_hd, ny_hd), 2, (nose_color[0], nose_color[1], nose_color[2], 255), -1)

    cv2.imwrite(output_path, rgba)
    print(f"Final Surgical Reconstruction complete: {output_path}")

# Run on the latest provided image
ultimate_surgical_fixed_nose("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
