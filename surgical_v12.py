import cv2
import numpy as np

def surgical_v12_masterpiece(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]

    # 1. Face Coordinates (Corrected for 324x211)
    fx, fy = 163, 62
    
    # Sample skin
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # 2. DIGITAL SURGERY
    # Patch Mouth
    cv2.circle(img, (fx, fy + 11), 1, skin_color, -1)
    # Add Robust Anime Nose
    # We use a 2x2 dark block to make it clearly visible
    nose_color = (np.array(skin_color) * 0.65).astype(np.uint8).tolist()
    cv2.rectangle(img, (fx, fy + 4), (fx + 1, fy + 5), nose_color, -1)

    # 3. BACKGROUND OBLITERATION (Clean Fill)
    # Convert to high-contrast for fill
    # Target the white/gray checkers.
    # We will fill from the corners.
    mask = np.zeros((h+2, w+2), np.uint8)
    fill_color = [255, 0, 255] # Magenta (not in unit)
    
    # Fill from all corners and edges to find the exterior
    for x in [0, w-1]:
        for y in range(h):
            if np.all(img[y, x] > 180): # If it looks like background
                cv2.floodFill(img, mask, (x, y), fill_color, (15, 15, 15), (15, 15, 15))
    for y in [0, h-1]:
        for x in range(w):
            if np.all(img[y, x] > 180):
                cv2.floodFill(img, mask, (x, y), fill_color, (15, 15, 15), (15, 15, 15))

    # 4. Transparency Nuke
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Anything Magenta is now background
    bg_mask = (img[:,:,0] == fill_color[0]) & (img[:,:,1] == fill_color[1]) & (img[:,:,2] == fill_color[2])
    rgba[bg_mask, 3] = 0
    
    # Special: Kill any leftover absolute white/light-grey checkers inside gaps
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    inner_bg = (hsv[:,:,1] < 40) & (hsv[:,:,2] > 200)
    
    # PROTECTION: Character core must remain solid
    # Face & Body (centered around fx, fy)
    protection = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(protection, (140, 20), (190, 85), 255, -1) # Face
    cv2.rectangle(protection, (100, 85), (220, 190), 255, -1) # Body/Armor
    
    # Apply inner transparency but only if NOT in protection zone
    rgba[inner_bg & (protection == 0), 3] = 0
    rgba[protection == 255, 3] = 255 # Guarantee core is solid

    # 5. Physics: Remove the "1600" tag and black Corners
    # Crop 10 pixels off each side
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]

    # 6. HD RECONSTRUCTION (4x Lanczos)
    final = cv2.resize(rgba, (nw*4, nh*4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Surgical V12 Masterpiece complete: {output_path}")

surgical_v12_masterpiece("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
