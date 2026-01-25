import cv2
import numpy as np

def final_surgical_cleanup(input_path, output_path):
    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not read {input_path}")
        return

    # If it doesn't have an alpha channel, add one
    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        a = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge([b, g, r, a])
    
    b, g, r, a = cv2.split(img)
    
    # 1. REMOVE DIAMOND (Bottom Right)
    # Wiping a larger 80x80 area to be absolutely sure
    h, w = a.shape
    a[h-80:, w-80:] = 0
    
    # 2. TARGET THE CHECKERBOARD
    # The checkers in Gemini are usually:
    # Color 1: ~ (0, 0, 0)
    # Color 2: ~ (102, 102, 102)
    
    # Create mask for Background color 1 (Blacks/Dark grays)
    # Saturated colors (character) usually have high R and low B/G or vice versa.
    # Checkers are neutral (R~G~B)
    is_neutral = (np.abs(r.astype(int) - g.astype(int)) < 15) & (np.abs(g.astype(int) - b.astype(int)) < 15)
    
    dark_checkers = (r < 60) & (g < 60) & (b < 60) & is_neutral
    gray_checkers = (r > 70) & (r < 150) & (g > 70) & (g < 150) & (b > 70) & (b < 150) & is_neutral
    
    bg_mask = dark_checkers | gray_checkers
    
    # Use flood fill to only remove bg_mask connected to the edges
    # This protects neutral colors inside the character (if any)
    flood_mask = bg_mask.astype(np.uint8) * 255
    # Add a 1px border to ensure connectivity
    padded = cv2.copyMakeBorder(flood_mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=255)
    
    # Flood fill from all edges
    h_p, w_p = padded.shape
    for x in range(w_p):
        if padded[0, x] == 255: cv2.floodFill(padded, None, (x, 0), 128)
        if padded[h_p-1, x] == 255: cv2.floodFill(padded, None, (x, h_p-1), 128)
    for y in range(h_p):
        if padded[y, 0] == 255: cv2.floodFill(padded, None, (0, y), 128)
        if padded[y, w_p-1] == 255: cv2.floodFill(padded, None, (w_p-1, y), 128)
        
    # Pixels marked 128 are confirmed background
    confirmed_bg = (padded[1:-1, 1:-1] == 128)
    
    # Optional: Dilate the background mask slightly to get rid of the "halo"
    kernel = np.ones((3,3), np.uint8)
    confirmed_bg = cv2.dilate(confirmed_bg.astype(np.uint8), kernel, iterations=1).astype(bool)
    
    # Set alpha to 0 for confirmed background
    a[confirmed_bg] = 0
    
    # 3. CLEAN UP ISLANDS
    # Anything very small and transparent-ish or neutral near the sword
    # we can use a contour-based approach to keep only the largest component
    # but the character is often multiple components (hair bits).
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Aggressive clean completed: {output_path}")

final_surgical_cleanup("public/assets/gemini_unit.png", "public/assets/gemini_unit_clean.png")
