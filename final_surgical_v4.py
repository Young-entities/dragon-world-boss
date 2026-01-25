import cv2
import numpy as np

def surgical_v4_perfect_crop(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return

    # 1. Surgical Crop - Remove the black frame and tag
    # Original is (211, 324, 3)
    # We want to remove the outer rounded frame and bottom-right '1600' tag
    # Let's crop to just the character content
    img = img[8:211-12, 10:324-10] 
    h, w = img.shape[:2]

    # 2. Mouth Removal
    # Search for skin tone specifically in the center-top 
    # Coordinates in this new crop: Center x=152, y=60
    mouth_y, mouth_x = 51, 151
    skin_roi = img[mouth_y-8:mouth_y-3, mouth_x-5:mouth_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8)
    cv2.circle(img, (mouth_x, mouth_y), 1, skin_color.tolist(), -1)
    # definition check: nose should be just above
    
    # 3. Transparency & Backround Erasure (Targeting checkers)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_bg = np.array([0, 0, 200]) # White/Light-Grey range
    upper_bg = np.array([180, 55, 255])
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    char_mask = cv2.bitwise_not(bg_mask)
    
    # Target only the unit by refining based on blue/saturation
    # The character is very saturated (Vibrant Blue)
    blue_range = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([140, 255, 255]))
    # Combine - we want either something not gray OR something that is definitely blue
    char_mask = cv2.bitwise_or(char_mask, blue_range)

    # 4. Clean up
    kernel = np.ones((2,2), np.uint8)
    char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_CLOSE, kernel)
    char_mask = cv2.GaussianBlur(char_mask, (3,3), 0)

    # 5. Upscale and Polish
    img_big = cv2.resize(img, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    mask_big = cv2.resize(char_mask, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    
    b, g, r = cv2.split(img_big)
    rgba = cv2.merge([b, g, r, mask_big])
    
    cv2.imwrite(output_path, rgba)
    print(f"Perfect Surgical V4 completed: {output_path}")

surgical_v4_perfect_crop("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769301101122.png", "public/assets/water_deity_unit_final.png")
