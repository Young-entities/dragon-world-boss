import cv2
import numpy as np

def surgical_v27_solid_checker_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # 1. CHARACTER CORE (Color vs B&W checkers)
    # The unit is blues/cyans. The checkerboard is grey/white.
    # Saturation is the key.
    is_char = (s > 15) | (v < 150) # Keep colorful and dark bits
    
    # Fill internal holes (Closing)
    # This turns her face/skin area into a solid block for the alpha mask
    kernel = np.ones((25, 25), np.uint8)
    filled_mask = cv2.morphologyEx(is_char.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    
    # 2. EDGE FLOODFILL (Outer checkers)
    mask = np.zeros((h+2, w+2), np.uint8)
    temp_img = img.copy()
    fill_color = (255, 0, 255) # Magenta
    # High tolerance from corners
    pts = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1), (w//2, 0), (0, h//2), (w-1, h//2)]
    for pt in pts:
        cv2.floodFill(temp_img, mask, pt, fill_color, (45, 45, 45), (45, 45, 45))
    
    # 3. FINAL ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    
    # Rule 1: Outer background (FloodFilled)
    is_outer_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    alpha[is_outer_bg] = 0
    
    # Rule 2: Internal Checkers
    # (Low saturation, high value, AND not inside the filled char body)
    internal_checker = (s < 30) & (v > 180) & (filled_mask == 0)
    alpha[internal_checker] = 0
    
    # Rule 3: FACE PROTECTION (Manual hard-lock)
    fx, fy = 640, 241
    cv2.circle(alpha, (fx, fy), 100, 255, -1)
    # Core body protection
    cv2.rectangle(alpha, (500, 250), (780, 600), 255, -1)
    
    rgba[:,:,3] = alpha
    
    # 4. POLISH
    # Crop borders and watermark
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V27 Solid Checker nuke complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v27_solid_checker_nuke(source, "public/assets/water_deity_unit_final.png")
