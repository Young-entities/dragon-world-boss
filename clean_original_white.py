import cv2
import numpy as np

def clean_perfect_white(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # Target pure white areas
    # We use a slightly wider threshold because AI white can be like 254-255
    white_mask = (r > 245) & (g > 245) & (b > 245)
    
    # Flood fill starting from all corners to only get the background
    h, w = a.shape
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    
    seed_img = white_mask.astype(np.uint8) * 255
    # Flood from corners
    cv2.floodFill(seed_img, flood_mask, (0, 0), 128)
    cv2.floodFill(seed_img, flood_mask, (w-1, 0), 128)
    cv2.floodFill(seed_img, flood_mask, (0, h-1), 128)
    cv2.floodFill(seed_img, flood_mask, (w-1, h-1), 128)
    
    # Background is marked 128
    bg_mask = (seed_img == 128)
    
    # Set Alpha to 0
    a[bg_mask] = 0
    
    # Edge refinement (feather the edges slightly to remove white thin lines)
    kernel = np.ones((3,3), np.uint8)
    # Erode the character mask slightly
    char_mask = (a > 0).astype(np.uint8) * 255
    char_mask_eroded = cv2.erode(char_mask, kernel, iterations=1)
    
    a[char_mask_eroded == 0] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Perfectly cleaned original style character saved to {output_path}")

clean_perfect_white("public/assets/overlord_white_bg.png", "public/assets/overlord_perfect_transparent.png")
