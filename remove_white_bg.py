
import cv2
import numpy as np

def remove_white_background(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load {input_path}")
        return

    # Work on BGR img for floodfill
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill from (0,0)
    # Using a small tolerance to catch compression artifacts near white
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    cv2.floodFill(img, mask, (0,0), (0,0,0), (10,10,10), (10,10,10), flood_flags)
    
    # Floodfill other corners just in case
    cv2.floodFill(img, mask, (w-1,0), (0,0,0), (10,10,10), (10,10,10), flood_flags)
    cv2.floodFill(img, mask, (0,h-1), (0,0,0), (10,10,10), (10,10,10), flood_flags)
    cv2.floodFill(img, mask, (w-1,h-1), (0,0,0), (10,10,10), (10,10,10), flood_flags)
    
    # Extract the mask (remove borders)
    bg_mask = mask[1:-1, 1:-1]
    
    # Create RGBA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Set alpha: Background (255) -> 0, Foreground (0) -> 255
    rgba[:, :, 3] = cv2.bitwise_not(bg_mask)
    
    cv2.imwrite(output_path, rgba)
    print(f"Processed transparency for {output_path}")

remove_white_background("public/assets/eternal_lion_emperor.png", "public/assets/eternal_lion_emperor.png")
