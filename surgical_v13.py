import cv2
import numpy as np

def surgical_v13_floodfill(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # 1. FACIAL WORK (Manual fix)
    # Target face center: x=163, y=55 roughly
    fx, fy = 163, 62
    
    # Sample skin tone
    skin_roi = img[fy-10:fy-5, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Add Nose & Remove Mouth
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1) # mouth
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    cv2.circle(img, (fx, fy + 5), 1, nose_color, -1) # nose

    # 2. FLOOD FILL TRANSPARENCY
    # We turn the image into BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # We use floodfill to identify the background.
    # We fill from the top-left corner (usually background)
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill with a dummy color (Magenta) to find connected background
    temp_img = img.copy()
    fill_color = (255, 0, 255)
    
    # Fill from corners
    cv2.floodFill(temp_img, mask, (0,0), fill_color, (20,20,20), (20,20,20))
    cv2.floodFill(temp_img, mask, (w-1, 0), fill_color, (20,20,20), (20,20,20))
    
    # Apply results to alpha channel
    bg_mask = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    rgba[bg_mask, 3] = 0
    
    # 3. SPRITE POLISH
    # Crop borders
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    
    # HD Reconstruction
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Surgical Floodfill complete: {output_path}")

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
surgical_v13_floodfill(source, "public/assets/water_deity_unit_final.png")
