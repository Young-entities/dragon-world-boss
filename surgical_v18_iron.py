import cv2
import numpy as np

def surgical_v18_iron_solid_clean(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # 1. FACIAL RECONSTRUCTION (Surgical)
    # High-res coordinates (approx 1312x800)
    fx, fy = 654, 252 
    
    # Sample skin tone
    skin_roi = img[fy-30:fy-15, fx-20:fx+20]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove mouth
    cv2.circle(img, (fx, fy + 45), 8, skin_color, -1)
    
    # Add DEFINED NOSE (Elite shadow style)
    nose_shadow = (np.array(skin_color) * 0.55).astype(np.uint8).tolist()
    pts = np.array([[fx, fy + 15], [fx+5, fy + 28], [fx, fy + 25]], np.int32)
    cv2.fillPoly(img, [pts], nose_shadow)

    # 2. DEFINED PROTECTION MASK
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (590, 150), (715, 360), 255, -1) # Head
    cv2.rectangle(protection, (520, 360), (780, 580), 255, -1) # Body Core
    
    # 3. BACKGROUND ERASE (White & Checker segments)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Target low saturation (< 50) and high value (> 220)
    bg_mask = (s < 55) & (v > 220)
    
    # 4. Alpha Calculation
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask & (protection == 0)] = 0
    alpha[protection == 255] = 255
    
    # 5. NOISE REMOVAL (Clean floating artifacts)
    # Target small white islands in the alpha channel
    kernel = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel) # Removes small dots
    
    # 6. ASSET POLISH
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])
    
    # Crop borders and watermark
    rgba = rgba[30:760, 50:1260]
    
    # Final HD Save
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V18 Iron Solid Clean complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
surgical_v18_iron_solid_clean(source, "public/assets/water_deity_unit_final.png")
