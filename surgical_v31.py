import cv2
import numpy as np

def surgical_v35_bulletproof_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. TARGET THE EXACT COLORS OF THE CHECKERBOARD
    # I've sampled these from the latest fy33jn image
    # White tile: (255, 255, 255)
    # Grey tile: (240, 240, 240)
    
    # We use a very tight tolerance (5) to ensure we don't hit the character's blue
    white_tiles = cv2.inRange(img, (248, 248, 248), (255, 255, 255))
    grey_tiles = cv2.inRange(img, (235, 235, 235), (245, 245, 245))
    
    total_bg = white_tiles | grey_tiles
    
    # 2. SEAMLESS CLEANUP (The thin lines between tiles)
    # Grid lines where tiles meet might be slightly different.
    # We'll use a tiny dilation to swallow the grid lines.
    kernel = np.ones((3,3), np.uint8)
    total_bg = cv2.dilate(total_bg, kernel, iterations=1)
    
    # 3. FACIAL RECONSTRUCTION (The Face Protection)
    # Ensure no internal character colors are eaten
    shield = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(shield, (640, 241), 95, 255, -1) # Face core
    cv2.rectangle(shield, (520, 320), (760, 580), 255, -1) # Torso core
    
    # 4. FINAL ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency = Is Checker AND is NOT protected
    alpha[(total_bg == 255) & (shield == 0)] = 0
    # Force shield area to be solid
    alpha[shield == 255] = 255
    
    rgba[:,:,3] = alpha
    
    # 5. POLISH & CROP
    # Remove borders and bottom watermark
    rgba = rgba[18:h-45, 18:w-18]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V35 Bulletproof Nuke complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v35_bulletproof_nuke(source, "public/assets/water_deity_unit_final.png")
