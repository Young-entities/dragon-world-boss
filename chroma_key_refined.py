import cv2
import numpy as np

def refine_chroma_key(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 1. Broaden the Green Range to catch fringes
    # Previous: 35-85.
    # Widen to 30-90?
    lower_green = np.array([30, 80, 80])
    upper_green = np.array([95, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert (Keep foreground)
    mask_inv = cv2.bitwise_not(mask)
    
    # 2. ERODE the mask to cut off green halo (1 pixel)
    kernel = np.ones((3,3), np.uint8)
    # Erode the FOREGROUND mask (mask_inv)
    mask_inv = cv2.erode(mask_inv, kernel, iterations=1)
    
    # Soften
    mask_inv = cv2.GaussianBlur(mask_inv, (1, 1), 0)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, mask_inv])
    
    cv2.imwrite(output_path, rgba)
    print(f"Refined Chroma Key (Halo Removed): {output_path}")

refine_chroma_key("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_azaerth_greenscreen_regen_1769702009898.png", "public/assets/dark_deity_unit.png")
