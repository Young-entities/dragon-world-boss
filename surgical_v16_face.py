import cv2
import numpy as np

def surgical_v16_final_face(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    # Face center is roughly fx=163, fy=62 in original 324x211
    fx, fy = 163, 62

    # 1. FACIAL RECONSTRUCTION
    # Sample skin tone from a safe area (forehead)
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Remove mouth - paint with skin color
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    
    # Add Pronounced Anime Nose shadow
    # Darker skin tone for the nose
    nose_color = (np.array(skin_color) * 0.50).astype(np.uint8).tolist()
    # Draw a 2x2 triangle/dot for the nose tip
    cv2.rectangle(img, (fx, fy + 4), (fx + 1, fy + 5), nose_color, -1)

    # 2. DEFINED PROTECTION MASK (The Sacred Unit)
    # 0 = background, 255 = keep
    protection = np.zeros((h, w), dtype=np.uint8)
    
    # Core Character Protection Zone (Guaranteed Solid)
    # Head/Face: x: 145-185, y: 30-85
    cv2.rectangle(protection, (145, 30), (185, 85), 255, -1)
    # Body/Torso: x: 120-210, y: 85-180
    cv2.rectangle(protection, (120, 85), (210, 180), 255, -1)
    
    # Dragons & Armor Protection (Saturated blue area)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Protect anything saturated blue
    blue_mask = cv2.inRange(hsv, np.array([85, 40, 40]), np.array([150, 255, 255]))
    protection = cv2.bitwise_or(protection, blue_mask)

    # 3. BACKGROUND ERASE (Checkers Only)
    # The checkers are Grey/White (Low Saturation, High Value)
    bg_candidates = (s < 50) & (v > 160)
    
    # 4. Alpha Calculation
    # Start fully opaque
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # If it looks like background AND it's not protected, make it transparent
    alpha[bg_candidates & (protection == 0)] = 0
    
    # 5. Clean Up Alpha
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # 6. ASSET POLISH (Merge)
    # Use the original image (with nose/mouth fix) and append alpha
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    rgba[:,:,3] = alpha
    
    # 7. Final Framing (Nuke the border and 1600 tag)
    # Crop: 8px off the top/sides, 10px off the bottom
    rgba = rgba[8:h-12, 10:w-10]
    nh, nw = rgba.shape[:2]
    
    # 8. Upscale to 4K Master (4x)
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Surgical V16 Final Face Solidified: {output_path}")

# Run on the latest provided image from user
user_image = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v16_final_face(user_image, "public/assets/water_deity_unit_final.png")
