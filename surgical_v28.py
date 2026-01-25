import cv2
import numpy as np

def surgical_v28_pure_checker_flood(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. FLOOD FILL FROM CORNERS
    # We use a tolerance of 55 to catch the entire checkered pattern (white + grey tiles)
    # This shouldn't eat the blue character if she is separated from the edges by checkers.
    mask = np.zeros((h+2, w+2), np.uint8)
    temp_img = img.copy()
    fill_color = (255, 0, 255) # Magenta
    
    # Corners and edges
    pts = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1), (w//2, 0), (0, h//2)]
    for pt in pts:
        cv2.floodFill(temp_img, mask, pt, fill_color, (55, 55, 55), (55, 55, 55))
    
    # 2. INTERNAL CHECKER REMOVAL (Floodfill from inner white gaps)
    # We find pixels that are definitely part of the checkerboard (low saturation, high value)
    # and not connected to the outer edge, and floodfill them too.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Checkers: S < 20, V > 200
    checker_seed_mask = (s < 20) & (v > 200)
    
    # We only floodfill internal seeds if they are not near the face (approx 640x241)
    # To keep the character solid.
    for y in range(0, h, 10):
        for x in range(0, w, 10):
            if checker_seed_mask[y, x] and temp_img[y, x, 1] != 0: # Not already filled
                # Distance from face check
                dist = np.sqrt((x-640)**2 + (y-241)**2)
                if dist > 150: # Only fill if far from character core
                    cv2.floodFill(temp_img, mask, (x, y), fill_color, (30, 30, 30), (30, 30, 30))
    
    # 3. Apply Transparency
    is_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    rgba[is_bg, 3] = 0
    
    # 4. POLISH
    rgba = rgba[15:h-45, 15:w-15]
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V28 Checker Flood complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fy33jnfy33jnfy33.png"
surgical_v28_pure_checker_flood(source, "public/assets/water_deity_unit_final.png")
