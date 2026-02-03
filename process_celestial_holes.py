
import cv2
import numpy as np

def remove_green_holes(input_path, output_path):
    print(f"Removing green holes from: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Target Neon Green: Low Red, High Green, Low Blue
    # BGR format in OpenCV
    # B < 60, G > 180, R < 60
    
    b, g, r, a = cv2.split(img)
    
    # Mask for Green Background
    mask_green = (b < 60) & (g > 180) & (r < 60)
    
    # Set Alpha to 0 where mask is True
    img[mask_green, 3] = 0
    
    # Optional: Soften edges? 
    # For now, hard cut is better than leaving green.
    
    # Crop
    coords = cv2.findNonZero(cv2.bitwise_not(mask_green.astype(np.uint8)))
    if coords is not None:
        x, y, w_rect, h_rect = cv2.boundingRect(coords)
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w_rect + pad)
        y2 = min(img.shape[0], y + h_rect + pad)
        img = img[y1:y2, x1:x2]
        print(f"Cropped to {x2-x1}x{y2-y1}")
        
    cv2.imwrite(output_path, img)
    print(f"Saved to {output_path}")

original_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/angel_lancer_no_fish_v1_1769739462457.png"
output_path = "public/assets/celestial_valkyrie.png"

remove_green_holes(original_path, output_path)
