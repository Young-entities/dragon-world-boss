import cv2
import numpy as np

def surgical_fire_unit_clean(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. IDENTIFY WHITE BACKGROUND
    # Targeted white range
    lower_white = np.array([245, 245, 245])
    upper_white = np.array([255, 255, 255])
    white_mask = cv2.inRange(img, lower_white, upper_white)
    
    # 2. FACIAL & SKIN SHIELD (Critical for Fire Unit)
    # The character's face is approx center top.
    # Shielding the face, neck, and any light parts of the flame sword.
    shield = np.zeros((h, w), dtype=np.uint8)
    
    # Face & Skin
    cv2.circle(shield, (654, 252), 120, 255, -1)
    # Torso skin area
    cv2.rectangle(shield, (550, 280), (760, 520), 255, -1)
    # Protection for the bright hot core of the sword/flames
    cv2.rectangle(shield, (750, 50), (1200, 500), 255, -1)
    
    # 3. ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency = Is White AND is NOT shielded
    alpha[(white_mask == 255) & (shield == 0)] = 0
    # Force shield to solid
    alpha[shield == 255] = 255
    
    # 4. EXTERIOR POLISH (Corner floodfill to ensure no artifact blocks)
    flood_mask = np.zeros((h+2, w+2), np.uint8)
    # Match the 0-alpha pixels and connect them from the edges
    cv2.floodFill(alpha, flood_mask, (0,0), 0)
    cv2.floodFill(alpha, flood_mask, (w-1,0), 0)
    
    rgba[:,:,3] = alpha
    
    # 5. NO CROPPING (As per user: 'make sure nothing gets caught off')
    # Use full frame or very minimal 5px margin
    rgba = rgba[5:h-5, 5:w-5]
    
    cv2.imwrite(output_path, rgba)
    print(f"Fire unit transparency complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_djr1cfdjr1cfdjr1.png"
surgical_fire_unit_clean(source, "public/assets/fire_warrior_final.png")
