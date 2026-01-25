import cv2
import numpy as np

def surgical_v13_absolute_final(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # 0. High Quality Source
    h, w = img.shape[:2]
    
    # Coordinates in 324x211
    fx, fy = 163, 62

    # 1. FLOOD FILL PROTECTION MASK
    # We create a mask specifically to stop the flood fill from entering the face/unit
    # 0 = Fill can pass, 1 = Fill is blocked
    fill_mask = np.zeros((h+2, w+2), np.uint8)
    
    # Block the entire unit core
    # Mask coordinates are +1 relative to image
    cv2.rectangle(fill_mask, (140+1, 20+1), (195+1, 100+1), 1, -1) # Head
    cv2.rectangle(fill_mask, (100+1, 80+1), (230+1, 200+1), 1, -1) # Body
    
    # 2. INTEL FLOOD FILL
    # Fill from corners with tolerance 15
    fill_color = [255, 0, 255] # Magenta
    cv2.floodFill(img, fill_mask, (0,0), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(img, fill_mask, (w-1, 0), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(img, fill_mask, (0, h-1), fill_color, (15,15,15), (15,15,15))
    cv2.floodFill(img, fill_mask, (w-1, h-1), fill_color, (15,15,15), (15,15,15))

    # 3. FACIAL RECONSTRUCTION (Surgical)
    # Target skin color AFTER flood fill (since it protected the face)
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Patch Mouth
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    
    # Add DEFINED NOSE (Double-pixel shadow)
    nose_color = (np.array(skin_color) * 0.6).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 3), (fx + 1, fy + 4), nose_color, -1)

    # 4. TRANSPARENCY CONVERSION
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Nuke the Magenta background
    bg_mask = (img[:,:,0] == 255) & (img[:,:,1] == 0) & (img[:,:,2] == 255)
    rgba[bg_mask, 3] = 0
    
    # Nuke any pure white stickers left behind (conservative)
    white_mask = (img[:,:,0] > 250) & (img[:,:,1] > 250) & (img[:,:,2] > 250)
    # But ONLY if not in face
    face_protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(face_protection, (150, 40), (180, 80), 255, -1)
    rgba[white_mask & (face_protection == 0), 3] = 0

    # 5. FINAL POLISH
    # Crop borders
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    
    # Force solid face (no transparency)
    rgba_final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, rgba_final)
    print(f"Absolute Final Fixed Deity complete: {output_path}")

ultimate_surgical_fixed_nose_coords_v13 = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v13_absolute_final(ultimate_surgical_fixed_nose_coords_v13, "public/assets/water_deity_unit_final.png")
