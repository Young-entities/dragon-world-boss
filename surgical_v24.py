import cv2
import numpy as np

def surgical_v24_solid_hydra(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]

    # 1. CHARACTER DEFINITION (Color vs Greyscale)
    # The character (blue/cyan/skin) has color. The background is white/grey.
    # We use saturation to find the character.
    # S > 25 catches the water dragons and armor.
    # S < 25 are background pixels OR very light highlights.
    char_base = (s > 25) | (v < 150) # Catch colors and dark shadows
    
    # 2. FILL THE BODY (Closing)
    # This fills the light internal gaps (like face and eyes) that have low saturation.
    kernel = np.ones((15, 15), np.uint8)
    filled_mask = cv2.morphologyEx(char_base.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    
    # 3. EDGE CLEANING (Flood Fill)
    # We use floodfill on a temp image to identify the actual background.
    temp_img = img.copy()
    fill_mask = np.zeros((h+2, w+2), np.uint8)
    # High tolerance to swallow the white rectangular framing
    cv2.floodFill(temp_img, fill_mask, (0,0), (255, 0, 255), (40, 40, 40), (40, 40, 40))
    cv2.floodFill(temp_img, fill_mask, (w-1, 0), (255, 0, 255), (40, 40, 40), (40, 40, 40))
    
    is_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    
    # 4. FINAL ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency = (It is BG) OR (It is white-ish AND NOT in the filled character body)
    is_internal_hole = (s < 35) & (v > 190) & (filled_mask == 0)
    
    alpha[is_bg] = 0
    alpha[is_internal_hole] = 0
    
    # HARD PROTECTION: Face area must be solid
    cv2.circle(alpha, (654, 255), 85, 255, -1)
    
    rgba[:,:,3] = alpha

    # 5. CROP ARTIFACTS
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V24 Solid Hydra complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fm14x0fm14x0fm14.png"
surgical_v24_solid_hydra(source, "public/assets/water_deity_unit_final.png")
