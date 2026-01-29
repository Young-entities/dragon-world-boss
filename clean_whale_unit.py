import cv2
import numpy as np

def clean_bg(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold white
    _, alpha = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

    # Protection Mask
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(mask, (w//2, h//2), (int(w*0.4), int(h*0.4)), 0, 0, 360, 255, -1)
    
    alpha = cv2.bitwise_or(alpha, mask)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Cleaned Final Unit: {output_path}")

clean_bg("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/ocean_warlord_final_no_armor_1769651660904.png", "public/assets/ocean_king_poseidon.png")
