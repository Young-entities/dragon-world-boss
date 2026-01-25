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
    # Fire icon covers ~80% of its canvas (43/54).
    # We match that exactly here for perfect parity.
    padding = int(min(w, h) * 0.46)
    radius = int(padding * 0.80) 
    
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    rgba[:,:,3] = mask
    
    # Crop to a square canvas
    y_min, y_max = center[1] - padding, center[1] + padding
    x_min, x_max = center[0] - padding, center[0] + padding
    rgba = rgba[y_min:y_max, x_min:x_max]
    
    cv2.imwrite(output_path, rgba)
    print(f"Water Icon Matched to Fire Size: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_4ya7xl4ya7xl4ya7.png"
surgical_v50_clean_water_icon(source, "public/assets/element_water.png")
