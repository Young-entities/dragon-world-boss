import cv2
import numpy as np

def surgical_v50_clean_water_icon(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # The icon is a circle. We can just use a circular mask.
    center = (w // 2, h // 2)
    radius = int(min(w, h) * 0.38) # Added more padding to match Fire icon visual size
    
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Optional: Soften the edges a bit
    # mask = cv2.GaussianBlur(mask, (3, 3), 0)
    
    rgba[:,:,3] = mask
    
    # Crop to the circle
    x, y, r = center[0], center[1], radius
    rgba = rgba[y-r:y+r, x-r:x+r]
    
    cv2.imwrite(output_path, rgba)
    print(f"Water Icon Cleaned: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_4ya7xl4ya7xl4ya7.png"
surgical_v50_clean_water_icon(source, "public/assets/element_water.png")
