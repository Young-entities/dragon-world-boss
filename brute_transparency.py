import cv2
import numpy as np

def brute_force_transparency(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return

    # If it doesn't have an alpha channel, add one
    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        a = np.ones(b.shape, dtype=b.dtype) * 255
    else:
        b, g, r, a = cv2.split(img)

    # Convert to grayscale for easier thresholding
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    
    # Target anything that is pure white or very high light (the background)
    # Threshold at 230 - anything brighter than 230 becomes transparent
    _, mask = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY_INV)
    
    # Refine the character: we want to keep the vibrant blues even if they are bright
    # Let's use Saturation as a safeguard
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    # If a pixel is very saturated (vibrant), keep it! 
    # (Background checkers are gray/white, meaning Low Saturation)
    vibrant_mask = cv2.threshold(s, 20, 255, cv2.THRESH_BINARY)[1]
    
    # Final Alpha = (Is not white) OR (Is vibrant)
    final_alpha = cv2.bitwise_or(mask, vibrant_mask)
    
    # Edge Smoothing
    final_alpha = cv2.GaussianBlur(final_alpha, (3,3), 0)
    
    # Merge and save
    result = cv2.merge([b, g, r, final_alpha])
    cv2.imwrite(output_path, result)
    print(f"Brute force transparency completed: {output_path}")

brute_force_transparency("public/assets/water_deity_unit_final.png", "public/assets/water_deity_unit_final.png")
