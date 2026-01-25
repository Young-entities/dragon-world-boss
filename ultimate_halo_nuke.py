import cv2
import numpy as np

def surgical_v44_contour_isolation(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. FIND THE CHARACTER (Core Saturation)
    # The background is white (S=0). The character has color (S>10).
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # We define the character as anything with color OR darkness
    is_char = (s > 10) | (v < 150)
    
    # 2. CREATE A SOLID UNIT MASK (No gaps)
    # Use closing to connect the armor, face, and water into one giant block
    kernel = np.ones((25, 25), np.uint8)
    solid_unit = cv2.morphologyEx(is_char.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    
    # 3. SELECT THE MAIN UNIT CONTOUR
    # This identifies "The Body" and ignores all outside background.
    contours, _ = cv2.findContours(solid_unit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_body_mask = np.zeros_like(solid_unit)
    if contours:
        # Sort by area and keep the largest (the character cluster)
        for cnt in contours:
            if cv2.contourArea(cnt) > 20000: # Threshold for the main unit
                cv2.drawContours(main_body_mask, [cnt], -1, 255, -1)
    
    # 4. REMOVE WHITE "GAPS" INSIDE THE BODY
    # We only remove pixels that are white (S<20, V>200) AND inside the main body mask
    # BUT we must protect the face skin.
    internal_white = (s < 20) & (v > 200)
    
    # Face Protection Shield
    shield = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(shield, (654, 252), 100, 255, -1) # Protect the face skin
    
    # Assemble the final alpha
    alpha = np.zeros((h, w), dtype=np.uint8)
    # Start: The body is 255 (solid)
    alpha[main_body_mask == 255] = 255
    # Dissolve white-gaps inside the body IF not face
    alpha[internal_white & (main_body_mask == 255) & (shield == 0)] = 0
    
    rgba[:,:,3] = alpha
    
    # 5. CROP ARTIFACTS
    # Just the 15px border and bottom tag
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V44 Contour Isolation complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v44_contour_isolation(source, "public/assets/water_deity_unit_final.png")
