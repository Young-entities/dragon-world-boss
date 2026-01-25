import cv2
import numpy as np

def surgical_v29_contour_checker_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # 1. DEFINE CHARACTER PIXELS
    # Character has: Saturation (blues/cyans/skin) OR Darkness (armor shadows)
    # Background (checkers) has: 0 saturation AND High brightness
    
    # We define character as anything with a bit of color OR significant darkness
    is_char = (s > 18) | (v < 140)
    
    # 2. FILL INTERNAL HOLES (Morphological Closing)
    # This connects the armor, face, and water dragons into one solid mask
    kernel = np.ones((15, 15), np.uint8)
    alpha_mask = cv2.morphologyEx(is_char.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    
    # 3. SELECT MAIN UNIT CONTOUR
    # This wipes out any floating background tiles that our mask might have missed
    contours, _ = cv2.findContours(alpha_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean_alpha = np.zeros_like(alpha_mask)
    if contours:
        # Sort by area and take the largest (the character + dragons)
        for cnt in contours:
            if cv2.contourArea(cnt) > 5000: # Threshold to ignore small artifacts
                cv2.drawContours(clean_alpha, [cnt], -1, 255, -1)
    
    # 4. FINAL ASSEMBLY
    rgba[:,:,3] = clean_alpha
    
    # 5. POLISH & CROP
    # Crop borders and bottom watermark
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V29 Contour Checker nuke complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v29_contour_checker_nuke(source, "public/assets/water_deity_unit_final.png")
