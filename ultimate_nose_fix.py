import cv2
import numpy as np

def surgical_v6_pronounced_nose(input_path, output_path):
    # Load the high-res base image (the one with full spear)
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]

    # 1. Mouth Removal (Better cloning)
    # Target center: x=512, y=278 roughly
    face_zone = img[220:320, 480:540]
    # Patch mouth area with skin tone (median of above area)
    skin_color = np.median(face_zone[0:20, :].reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    # Fill mouth area
    cv2.rectangle(img, (496, 275), (510, 281), skin_color, -1)
    # Blend
    cv2.GaussianBlur(img[270:290, 490:520], (5,5), 0, dst=img[270:290, 490:520])

    # 2. DEFINED NOSE (The Big Fixed)
    # Anime noses are often a triangle shadow or a sharp corner.
    # We'll use a 3-point polygon to create a sharp, visible nose shadow.
    nose_x, nose_y = 502, 268 
    # Create a small, dark skin-tone color
    shadow_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    
    # Draw a distinct small vertical triangle shadow
    pts = np.array([[nose_x, nose_y], [nose_x+2, nose_y+4], [nose_x, nose_y+3]], np.int32)
    cv2.fillPoly(img, [pts], shadow_color)
    
    # 3. CLEAN WHITE BACKGROUND
    # Ensure background is ABSOLUTELY 255 white for transparency
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    img[mask == 255] = [255, 255, 255] # Force background pixels to absolute white

    # 4. Transparency Nuke
    # New BGRA merge
    gray_final = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(gray_final, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Protect face detail
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (450, 200), (580, 400), 255, -1)
    alpha = cv2.bitwise_or(alpha, protection)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V6 Pronounced Nose completed: {output_path}")

# Using the raw unedited master as base to ensure no old glitches carry over
surgical_v6_pronounced_nose("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_deity_nosed_white_bg_1769301126078.png", "public/assets/water_deity_unit_final.png")
