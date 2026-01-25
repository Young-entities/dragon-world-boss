import cv2
import numpy as np

def surgical_v30_aggressive_checker(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # 1. DEFINE BACKGROUND (Checkers)
    # Checkers (grey/white) have very low saturation and high value.
    # Unit (blue/cyan/skin) has color.
    is_checker = (s < 28) & (v > 160)
    
    # 2. DEFINE PROTECTION (Unit Core)
    # We want to protect the face and torso skin highlights which might be low-saturation.
    shield = np.zeros((h, w), dtype=np.uint8)
    # Scaled coordinates for 1280x832
    cv2.circle(shield, (640, 241), 90, 255, -1) # Face
    cv2.rectangle(shield, (520, 320), (760, 580), 255, -1) # Torso core
    
    # 3. ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency = Is Checker AND is NOT protected
    alpha[is_checker & (shield == 0)] = 0
    # Hard force shield
    alpha[shield == 255] = 255
    
    # 4. EXTERIOR CLEANUP (Corner FloodFill)
    # To ensure no floating artifacts near edges
    temp_img = img.copy()
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(temp_img, mask, (0,0), (255,0,255), (45, 45, 45), (45, 45, 45))
    is_outer_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    alpha[is_outer_bg] = 0
    
    rgba[:,:,3] = alpha
    
    # 5. POLISH & CROP
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V30 Aggressive Checker complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v30_aggressive_checker(source, "public/assets/water_deity_unit_final.png")
