import cv2
import numpy as np

def transparent_dot_fix(input_path, output_path):
    # Load the raw square icon to start fresh
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # 1. Target EVERY white/bright pixel for transparency
    # If all channels are very bright, it's definitely the "dot" or "background"
    white_mask = (r > 220) & (g > 220) & (b > 220)
    a[white_mask] = 0
    
    # 2. Extract the circle (same as before but stricter)
    h, w = a.shape
    center = (w // 2, h // 2)
    radius = int(min(h, w) * 0.42)
    mask = np.zeros((h, w), np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Final alpha is the intersection of the circle and non-white pixels
    a = cv2.bitwise_and(a, mask)
    
    # 3. Clean up loose pixels (erosion)
    kernel = np.ones((2,2), np.uint8)
    a = cv2.erode(a, kernel, iterations=1)
    
    # Standard V4 smoothing
    a = cv2.GaussianBlur(a, (3,3), 0)
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Transparency-based dot removal completed: {output_path}")

# Run on the source raw image
transparent_dot_fix("public/assets/icon_fire_raw.png", "public/assets/element_fire_v4.png")
