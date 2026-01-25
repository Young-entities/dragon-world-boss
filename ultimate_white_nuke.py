import cv2
import numpy as np

def surgical_v36_pure_white_clean(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. IDENTIFY WHITE BACKGROUND (Floating gaps + Outer area)
    # We target every pixel that is near-white.
    # In AI images with white BG, anything > 250 across RGB is usually background.
    lower_white = np.array([248, 248, 248])
    upper_white = np.array([255, 255, 255])
    
    white_mask = cv2.inRange(img, lower_white, upper_white)
    
    # 2. DEFINED PROTECTION SHIELD (Preserve the character artwork)
    # Even on a white background, her face/skin is close to white. 
    # We protect the central character core so no "holes" appear in her body.
    fx, fy = 654, 252 # High-res center (1312x800 base)
    shield = np.zeros((h, w), dtype=np.uint8)
    # Face & Neck
    cv2.circle(shield, (fx, fy), 100, 255, -1)
    # Torso/Arms core
    cv2.rectangle(shield, (550, 280), (760, 550), 255, -1)
    # Legs skin area
    cv2.rectangle(shield, (620, 550), (690, 750), 255, -1)
    
    # 3. ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency = Is White AND is NOT shielded
    alpha[(white_mask == 255) & (shield == 0)] = 0
    # Hard lock shield to solid
    alpha[shield == 255] = 255
    
    # 4. EXTERIOR POLISH (Corner floodfill to kill any remaining artifacts)
    # This specifically target the outer rectangular border.
    flood_mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(alpha, flood_mask, (0,0), 0)
    cv2.floodFill(alpha, flood_mask, (w-1,0), 0)
    cv2.floodFill(alpha, flood_mask, (0,h-1), 0)
    cv2.floodFill(alpha, flood_mask, (w-1,h-1), 0)
    
    rgba[:,:,3] = alpha
    
    # 5. CROP ARTIFACTS
    # Remove the rounded AI border and bottom black bar/tag (typically ~40px)
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V36 White Transparency complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v36_pure_white_clean(source, "public/assets/water_deity_unit_final.png")
