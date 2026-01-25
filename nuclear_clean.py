import cv2
import numpy as np

def nuclear_clean(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape
    
    # 1. Target Checkerboard Colors
    # Usually: Dark (35-45) and Mid-Gray (100-110)
    # They are always NEUTRAL (R=G=B)
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_neutral = (diff_rg < 12) & (diff_gb < 12)
    
    # Checker 1: Dark
    mask1 = (r < 55) & (g < 55) & (b < 55) & is_neutral
    # Checker 2: Mid-Gray
    mask2 = (r > 70) & (r < 140) & (g > 70) & (g < 140) & (b > 70) & (b < 140) & is_neutral
    
    checker_seeds = (mask1 | mask2).astype(np.uint8) * 255
    
    # 2. CONNECT THE TILES
    # Use a large dilation to bridge the gaps between checker tiles
    kernel = np.ones((15, 15), np.uint8)
    dilated = cv2.dilate(checker_seeds, kernel, iterations=1)
    
    # 3. IDENTIFY OUTER BACKGROUND
    # Flood fill from many points along the perimeter
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    bg_ocean = np.zeros_like(a)
    
    # Seed points along the edges
    seeds = []
    for x in range(0, w, 20):
        seeds.append((x, 0))
        seeds.append((x, h-1))
    for y in range(0, h, 20):
        seeds.append((0, y))
        seeds.append((w-1, y))
        
    for sx, sy in seeds:
        if dilated[sy, sx] == 255:
            cv2.floodFill(dilated, flood_mask, (sx, sy), 128)
            
    # Everything turned to 128 in 'dilated' is connected to the edge
    # AND part of the "potential background sheet"
    is_bg_ocean = (dilated == 128)
    
    # 4. PROTECT THE CHARACTER CORE
    # We create a shield for the face/torso area where checkers should never be removed 
    # unless they are definitely connected to the outside.
    # Actually, the flood fill ALREADY does this! 
    # It won't enter the character unless there's a neutral-color "bridge" into the face.
    # To be safe, skip any pixel that is highly saturated (Character's skin/fire)
    # Skin has moderate saturation. Neutral patterns have almost zero.
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    is_saturated = (s > 15) # Character details have color
    
    # 5. FINAL CLEARANCE
    # Clear if it's in the background ocean AND has very low saturation (is a checker)
    vibrant_mask = (s < 12) & is_bg_ocean
    
    # Hard wipe the AI logo in bottom right (larger area)
    a[vibrant_mask] = 0
    a[h-90:, w-90:] = 0 
    
    # 6. EDGE SMOOTHING
    # Let's do a slight erosion on the alpha to kill the halo
    kernel_small = np.ones((3,3), np.uint8)
    # Mask of the character
    char_mask = (a > 0).astype(np.uint8) * 255
    char_mask = cv2.erode(char_mask, kernel_small, iterations=1)
    a[char_mask == 0] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print("Nuclear surgical cleanup: Floodfilled through dilated bridges.")

nuclear_clean("public/assets/gemini_unit.png", "public/assets/gemini_unit_clean.png")
