
import cv2
import numpy as np

def make_green_transparent(input_path, output_path):
    print(f"Processing: {input_path}")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Detect Green
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Set Alpha
    # Where mask is green (255), set alpha to 0
    img[mask > 0, 3] = 0
    
    cv2.imwrite(output_path, img)
    print(f"Saved to {output_path}")

make_green_transparent("public/assets/fire_empress_fix.png", "public/assets/fire_empress_fix.png")
