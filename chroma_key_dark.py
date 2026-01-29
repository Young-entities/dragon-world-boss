import cv2
import numpy as np

def chroma_key_remove(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Green Screen Range (Neon Green)
    # The generated image background is very bright green (approx 0, 255, 0).
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert Mask (Keep everything else)
    mask_inv = cv2.bitwise_not(mask)
    
    # Soften Edges / Anti-alias
    mask_inv = cv2.GaussianBlur(mask_inv, (1, 1), 0)
    
    # Also remove stray green pixels at edges?
    # Maybe erode slightly?
    # mask_inv = cv2.erode(mask_inv, None, iterations=1)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, mask_inv])
    
    cv2.imwrite(output_path, rgba)
    print(f"Updated Asset with New Gen: {output_path}")

chroma_key_remove("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_azaerth_greenscreen_regen_1769702009898.png", "public/assets/dark_deity_unit.png")
