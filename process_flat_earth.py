
import cv2
import numpy as np

def process_flat_earth_icon():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_element_flat_style_raw_1769882190739.png"
    out_base = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth.png"
    out_circle = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth_circle.png"
    
    print(f"Processing flat Earth icon from {src}...")
    img = cv2.imread(src)
    if img is None:
        print("Source image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # 1. White background removal using thresholding and contours
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    
    # Find the outermost circular contour
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found.")
        return
        
    main_cnt = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(main_cnt)
    center = (int(x), int(y))
    radius = int(radius)
    
    # Create mask for the circle (including the thick black border)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Update alpha channel
    img[:, :, 3] = mask
    
    # 2. Crop to the circle
    side = int(radius * 2)
    x1 = max(0, center[0] - radius)
    y1 = max(0, center[1] - radius)
    cropped = img[y1:y1+side, x1:x1+side]
    
    # 3. Standardize to 128x128
    final_icon = cv2.resize(cropped, (128, 128), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(out_base, final_icon)
    cv2.imwrite(out_circle, final_icon)
    print(f"Successfully saved flat Earth icon to {out_base}")

if __name__ == "__main__":
    process_flat_earth_icon()
