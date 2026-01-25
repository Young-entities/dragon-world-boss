import cv2
import numpy as np

def surgical_v26_high_res_checker_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. FLOOD FILL FROM CORNERS
    mask = np.zeros((h+2, w+2), np.uint8)
    temp_img = img.copy()
    fill_color = (255, 0, 255) # Magenta
    
    # High-res tolerance
    pts = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1), (w//2, 0), (0, h//2), (w-1, h//2)]
    for pt in pts:
        cv2.floodFill(temp_img, mask, pt, fill_color, (30, 30, 30), (30, 30, 30))
    
    # 2. INTERNAL CHECKER NUKE (HSV)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Checkers: Low saturation and High value
    internal_checker = (s < 25) & (v > 180)
    
    # 3. HIGH-RES PROTECTION (Face & Core)
    # Based on 1280x832
    fx, fy = 640, 241
    shield = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(shield, (fx, fy), 80, 255, -1) # Protect face
    cv2.rectangle(shield, (580, 320), (700, 500), 255, -1) # Protect upper torso/chest skin area
    
    # 4. FINAL ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    
    # Rule 1: Outer background
    is_outer_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    alpha[is_outer_bg] = 0
    
    # Rule 2: Internal checkers (not shielded)
    alpha[internal_checker & (shield == 0)] = 0
    
    # Rule 3: Forced protection
    alpha[shield == 255] = 255
    
    # 5. CROP ARTIFACTS
    rgba[:,:,3] = alpha
    # Remove borders and watermark (if any)
    # The image has a black bar at the very bottom typically in these gens
    rgba = rgba[10:h-45, 10:w-10]
    
    cv2.imwrite(output_path, rgba)
    print(f"High-Res Checkerboard dissolved: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v26_high_res_checker_nuke(source, "public/assets/water_deity_unit_final.png")
