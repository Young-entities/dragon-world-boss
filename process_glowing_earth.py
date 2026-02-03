
import cv2
import numpy as np

def process_glowing_earth_icon():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_element_icon_glow_raw_1769881801302.png"
    out_base = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth.png"
    out_circle = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth_circle.png"
    
    print(f"Processing glowing Earth icon from {src}...")
    img = cv2.imread(src)
    if img is None:
        print("Source image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # 1. Identify the circle by finding the outer black border
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    
    # Use adaptive threshold to handle the white background vs common icon colors
    _, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found.")
        return
        
    main_cnt = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(main_cnt)
    center = (int(x), int(y))
    radius = int(radius)
    
    # 2. Create high-quality circular mask
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Set transparency
    img[:, :, 3] = mask
    
    # 3. Crop to the circle
    # Add a tiny buffer to avoid edge artifacts
    side = int(radius * 2)
    x1 = max(0, int(center[0] - radius))
    y1 = max(0, int(center[1] - radius))
    cropped = img[y1:y1+side, x1:x1+side]
    
    # 4. Standardize to 128x128
    final_icon = cv2.resize(cropped, (128, 128), interpolation=cv2.INTER_LANCZOS4)
    
    # Save both versions
    cv2.imwrite(out_base, final_icon)
    cv2.imwrite(out_circle, final_icon)
    print(f"Successfully saved new glowing Earth icon to {out_base}")

if __name__ == "__main__":
    process_glowing_earth_icon()
