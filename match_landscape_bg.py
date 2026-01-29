import cv2
import numpy as np

def make_landscape_bg(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Source BG not found")
        return

    h, w = img.shape[:2]
    # Target Landscape 3:2 (Width > Height) like Nereid
    # If W=1024, H should be ~682
    
    target_h = int(w * 0.666)
    
    if target_h < h:
        start_y = (h - target_h) // 2
        crop = img[start_y:start_y+target_h, 0:w]
        cv2.imwrite(output_path, crop)
        print(f"Cropped BG to Landscape (3:2): {output_path}")
    else:
        # If already wide, crop width?
        print("Image is already wide enough?")
        cv2.imwrite(output_path, img)

make_landscape_bg("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_void_background_1769702147823.png", "public/assets/dark_void_bg.png")
