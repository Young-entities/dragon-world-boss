import cv2
import numpy as np

def use_uploaded_icon():
    input_path = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769717198444.png"
    output_path = "public/assets/fire_empress_icon.png"
    
    img = cv2.imread(input_path)
    if img is None:
        print("Icon load failed")
        return
        
    # Resize to 100x100
    resized = cv2.resize(img, (100, 100), interpolation=cv2.INTER_AREA)
    
    cv2.imwrite(output_path, resized)
    print(f"Icon Updated Direct: {output_path}")

use_uploaded_icon()
