import cv2
import numpy as np

def anti_checker_fix(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    b, g, r, a = cv2.split(img)
    
    # Target the checkers: they are high-value, low-saturation.
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Checkers are very gray (s < 30) and very bright (v > 200)
    # Let's wipe everything that matches this
    checker_mask = (s < 45) & (v > 180)
    
    # New Alpha: If it's a checker, it's 0. Otherwise keep current alpha
    a[checker_mask] = 0
    
    # Final cleanup: keep the core unit
    # Blue unit: (H 100-140)
    unit_core = (s > 50) & (v > 50)
    a[unit_core] = 255
    
    # Blend edges
    a = cv2.GaussianBlur(a, (3,3), 0)
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Anti-checker surgical fix completed: {output_path}")

anti_checker_fix("public/assets/water_deity_unit_final.png", "public/assets/water_deity_unit_final.png")
