
import cv2
import numpy as np

def clean_earth_contours():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Cleaning Earth Unit Contours from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    if img.shape[2] < 4:
        print("No alpha, converting")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
    # Extract Alpha
    alpha = img[:, :, 3]
    
    # Threshold Alpha to Binary
    _, binary = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
    
    # Find Contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No contours found")
        return
        
    # Find Largest Contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Create Mask for Largest Contour
    mask = np.zeros_like(alpha)
    cv2.drawContours(mask, [largest_contour], -1, 255, -1)
    
    # Apply Mask (Keep only largest blob)
    # This deletes floating white debris
    img = cv2.bitwise_and(img, img, mask=mask)
    
    # Erode Alpha (Shrink edges)
    # This removes white potential fringes
    kernel = np.ones((3,3), np.uint8) # 3x3 kernel erodes ~1px radius
    eroded_alpha = cv2.erode(img[:, :, 3], kernel, iterations=1)
    
    img[:, :, 3] = eroded_alpha
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Largest Contour + Erosion)")

clean_earth_contours()
