import cv2
import numpy as np

def update_icon(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Resize/Crop to Square
    h, w = img.shape[:2]
    # If user provided a rectangle, crop center square
    min_dim = min(h, w)
    
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    
    crop = img[start_y:start_y+min_dim, start_x:start_x+min_dim]
    
    # Resize to 200x200
    resized = cv2.resize(crop, (200, 200), interpolation=cv2.INTER_AREA)
    
    cv2.imwrite(output_path, resized)
    print(f"Updated Icon: {output_path}")

update_icon("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769652915955.png", "public/assets/dark_deity_icon.png")
