import cv2
import numpy as np

def clean_final_dark(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Convert to grayscale for thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold strictly (High brightness = Background)
    # Background is likely pure white (255) or very close.
    # Set threshold to 250.
    _, mask_bg = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    
    # Invert mask (Background is 0, potential foreground is 255)
    mask_fg = cv2.bitwise_not(mask_bg)
    
    # PROTECTION:
    # 1. Protect Center (Character Body)
    h, w = img.shape[:2]
    protection_mask = np.zeros((h, w), dtype=np.uint8)
    # Ellipse covering body
    cv2.ellipse(protection_mask, (w//2, h//2 + 20), (int(w*0.4), int(h*0.45)), 0, 0, 360, 255, -1)
    
    # 2. Add Protection to Foreground Mask
    final_alpha = cv2.bitwise_or(mask_fg, protection_mask)
    
    # 3. Soften Edges
    final_alpha = cv2.GaussianBlur(final_alpha, (3, 3), 0)
    
    # 4. Create RGBA
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, final_alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Final Clean Complete: {output_path}")

clean_final_dark("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769653792914.png", "public/assets/dark_deity_unit.png")
