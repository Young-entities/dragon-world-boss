import cv2
import numpy as np

def clean_dark_unit(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # 1. Remove Top Text (approx top 80 pixels)
    # Paint it white so it becomes transparent
    img[0:80, :] = [255, 255, 255]
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold white background (near 250)
    _, alpha = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

    # Protection Mask (Center area)
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    # Ellipse in center to protect unit
    cv2.ellipse(mask, (w//2, h//2 + 30), (int(w*0.45), int(h*0.45)), 0, 0, 360, 255, -1)
    
    alpha = cv2.bitwise_or(alpha, mask)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Cleaned Dark Unit (Text Removed): {output_path}")

clean_dark_unit("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_primordial_warlord_retry_1769652328687.png", "public/assets/dark_deity_unit.png")
