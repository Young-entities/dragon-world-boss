
import cv2
import numpy as np

def clean_green_scribbles(input_path, output_path):
    print(f"Cleaning: {input_path}")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    # Convert to HSV to detect green
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define green range (Neon green is usually distinct)
    # Green is roughly 60 degrees. 
    # Range: 40-80?
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Dilate mask slightly to cover edges of scribbles
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # Inpaint
    # Use Telea algorithm
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    cv2.imwrite(output_path, result)
    print(f"Saved cleaned image to {output_path}")

clean_green_scribbles("public/assets/fire_bg_broken.png", "public/assets/fire_bg_fixed.png")
