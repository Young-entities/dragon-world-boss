import cv2
import numpy as np

def clean_white_bg(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    # Ensure 4 channels
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # Target WHITE (255, 255, 255)
    # We use a broad threshold for "off-white" as well
    white_mask = (r > 240) & (g > 240) & (b > 240)
    
    # Use flood fill from the edges to ensure we don't clear white bits inside the character (e.g. eyes or highlights)
    h, w = a.shape
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # Flood fill on the white_mask
    seed_mask = white_mask.astype(np.uint8) * 255
    cv2.floodFill(seed_mask, flood_mask, (0, 0), 128)
    cv2.floodFill(seed_mask, flood_mask, (w-1, 0), 128)
    cv2.floodFill(seed_mask, flood_mask, (0, h-1), 128)
    cv2.floodFill(seed_mask, flood_mask, (w-1, h-1), 128)
    
    # Confirmed BG is where the flood fill hit (marked 128)
    bg_mask = (seed_mask == 128)
    
    # Set Alpha to 0 for background
    a[bg_mask] = 0
    
    # Edge refining: dilate the transparent mask slightly to remove white halos
    kernel = np.ones((3,3), np.uint8)
    bg_dilated = cv2.dilate(bg_mask.astype(np.uint8), kernel, iterations=1)
    a[bg_dilated > 0] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Cleaned white background: {output_path}")

clean_white_bg("public/assets/new_overlord.png", "public/assets/new_overlord_transparent.png")
