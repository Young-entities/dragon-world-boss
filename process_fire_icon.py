import cv2
import numpy as np

def extract_fire_sphere(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    # Create center-based circular mask
    center = (w // 2, h // 2)
    # The circle in the image is almost full height, but has a bit of margin
    radius = int(min(h, w) * 0.44) 
    
    # Create 4-channel image
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Create black mask
    mask = np.zeros((h, w), np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Apply mask to alpha channel
    bgra[:, :, 3] = mask
    
    # Smooth the edges of the circle with a tiny bit of blur
    # but only on the alpha channel
    bgra[:, :, 3] = cv2.GaussianBlur(bgra[:, :, 3], (3, 3), 0)

    cv2.imwrite(output_path, bgra)
    print(f"Standardized Fire Sphere Icon saved: {output_path}")

extract_fire_sphere("public/assets/icon_fire_raw.png", "public/assets/icon_element_fire.png")
