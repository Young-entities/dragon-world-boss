import cv2
import numpy as np

def surgical_white_dissolve_v23_fixed(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. FACIAL PROTECTION SHIELD
    mask_face = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask_face, (654, 255), 85, 255, -1) 
    
    # 2. COLOR-BASED WHITE NUKE
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Target desaturated, bright pixels
    # Increase S threshold to catch more "off-white" pixels
    is_white = (s < 55) & (v > 175)
    
    # Apply transparency
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[is_white & (mask_face == 0)] = 0
    alpha[mask_face == 255] = 255
    
    # 3. FLOODFILL TO CLEAN EDGES
    # We use floodFill on a dummy 1-channel image to find everything connected to corners
    # This specifically kills the rectangular "blocks" near the edges.
    fill_mask = np.zeros((h+2, w+2), np.uint8)
    # Using the calculated alpha channel as a source for floodfilling
    # BUT floodFill needs a 2D array, which alpha is.
    # However, to be extra safe, we'll find outer white area using the original image.
    outer_bg = np.zeros((h, w), dtype=np.uint8)
    # Fill from corners in a temp BGR image
    temp_bgr = img.copy()
    cv2.floodFill(temp_bgr, fill_mask, (0,0), (255, 0, 255), (15, 15, 15), (15, 15, 15))
    cv2.floodFill(temp_bgr, fill_mask, (w-1, 0), (255, 0, 255), (15, 15, 15), (15, 15, 15))
    cv2.floodFill(temp_bgr, fill_mask, (0, h-1), (255, 0, 255), (15, 15, 15), (15, 15, 15))
    cv2.floodFill(temp_bgr, fill_mask, (w-1, h-1), (255, 0, 255), (15, 15, 15), (15, 15, 15))
    
    is_magenta = (temp_bgr[:,:,0] == 255) & (temp_bgr[:,:,1] == 0) & (temp_bgr[:,:,2] == 255)
    alpha[is_magenta] = 0
    
    rgba[:,:,3] = alpha

    # 4. FINAL CROP
    # Cut off 15px borders and the bottom black bar (roughly 40px)
    rgba = rgba[15:h-42, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"White background surgically nuked: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fm14x0fm14x0fm14.png"
surgical_white_dissolve_v23_fixed(source, "public/assets/water_deity_unit_final.png")
