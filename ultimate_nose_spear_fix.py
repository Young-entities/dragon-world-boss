import cv2
import numpy as np

def ultimate_final_fix(input_path, output_path):
    # Load original image with checkers and full spear
    img = cv2.imread(input_path)
    if img is None: return
    
    # 1. Surgical Crop - Remove black frame/corners
    # Original (211, 324)
    # The image has a white/gray checker background.
    # We'll crop to remove the outer black frame.
    img = img[5:206, 5:319] 
    h, w = img.shape[:2]

    # 2. DEFINED NOSE + MOUTH REMOVAL
    # Coordinates for this specific small image (roughly 320px wide)
    # Face center is at x=152, y=55 roughly.
    face_x = 152
    face_y = 53
    
    # Skin sample
    skin_roi = img[face_y-10:face_y-5, face_x-5:face_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove Mouth
    cv2.circle(img, (face_x, face_y + 10), 1, skin_color, -1)
    
    # Add Nose (subtle sharp dot/shadow)
    # A slightly darker pixel color
    nose_color = (np.array(skin_color) * 0.75).astype(np.uint8).tolist()
    # Draw a 1-pixel dot for the nose tip/shadow
    cv2.circle(img, (face_x, face_y + 4), 1, nose_color, -1)

    # 3. Checker Background Nuke (Aggressive)
    # Checkers are low-saturation high-value
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_bg = np.array([0, 0, 190]) 
    upper_bg = np.array([120, 60, 255])
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # Protect blue content (Dragons/Armor)
    # Blue is around Hue 100-140, Stat > 30
    blue_range = cv2.inRange(hsv, np.array([90, 40, 40]), np.array([150, 255, 255]))
    
    # Create Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask == 255] = 0
    alpha[blue_range == 255] = 255 # Safeguard for dragon translucent bits
    
    # Smooth alpha edges
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # 4. HD RECONSTRUCTION (Upscale 4x)
    # This makes the unit look premium in the game
    img_hd = cv2.resize(img, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
    mask_hd = cv2.resize(alpha, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
    
    b, g, r = cv2.split(img_hd)
    rgba = cv2.merge([b, g, r, mask_hd])
    
    cv2.imwrite(output_path, rgba)
    print(f"Ultimate Final Fix completed: {output_path}")

ultimate_final_fix("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312113083.png", "public/assets/water_deity_unit_final.png")
