
import cv2
import numpy as np

def fix_celestial_bg(path):
    print(f"Fixing background for: {path}")
    img = cv2.imread(path)
    if img is None:
        print("Error: Image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Robust Green Chroma Key in HSV
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    
    # Neon Green is approx Hue 60. Range 40-80 covers it well.
    # Saturation > 50, Value > 50 to avoid darks/whites.
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Set Alpha to 0 where mask is Green
    img[mask > 0, 3] = 0
    
    # Optional: Clean up edges with slight erosion of alpha? 
    # Let's keep it simple first.
    
    cv2.imwrite(path, img)
    print(f"Saved transparency fix to {path}")

fix_celestial_bg("public/assets/celestial_valkyrie.png")
