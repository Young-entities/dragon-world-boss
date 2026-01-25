import cv2
import numpy as np

def surgical_v12_debug(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]

    # Character center check
    # fx = 163, fy = 62
    # Let's paint a RED DOT at 163, 62 to verify position
    # cv2.circle(img, (163, 62), 2, (0, 0, 255), -1) 
    
    # Coordinates check: x=163 is approx center.
    # Face skin center: x=163, y=55 to 70.
    
    # 1. FACIAL SOLIDIFICATION
    # Sample skin tone
    skin_roi = img[50:60, 160:166]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # 2. DEFINED NOSE
    # Darker skin tone
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    
    # 3. TRANSPARENCY
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Target Checkers
    bg_mask = (s < 50) & (v > 180)
    
    # CORE PROTECTION ZONE
    # This covers the face, chest, and legs.
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (140, 35), (185, 90), 255, -1) # Face area
    cv2.rectangle(protection, (110, 90), (220, 200), 255, -1) # Body area
    
    # 4. FINAL ALPHA
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[bg_mask & (protection == 0)] = 0
    alpha[protection == 255] = 255 # Force Solid
    
    # 5. SPRITE CLEANUP
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])
    
    # Overwrite face area with solid skin color just to be ABSOLUTELY SURE
    # We do this specifically on the skin part (not hair)
    # The eyes should remain. So we only fill the mouth/nose area.
    cv2.rectangle(rgba, (158, 65), (168, 80), (skin_color[0], skin_color[1], skin_color[2], 255), -1)
    
    # Add Nose Shadow
    cv2.rectangle(rgba, (163, 68), (164, 70), (nose_color[0], nose_color[1], nose_color[2], 255), -1)

    # 6. Save HD
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Masterpiece solidified: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v12_debug(source, "public/assets/water_deity_unit_final.png")
