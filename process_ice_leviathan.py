
import cv2
import numpy as np

def process_monster_sprite(input_path, output_path):
    print(f"Processing: {input_path}")
    
    # 1. Load Image
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    h, w = img.shape[:2]

    # 2. Floodfill to create mask
    # Operate on BGR image
    # Seed points: corners
    seeds = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
    
    # Create a mask for floodfill (needs to be h+2, w+2)
    # 0 = background, 1 = foreground (initially)
    # We want to mark background.
    
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Green target approx (0, 255, 0) in BGR
    # Tolerance: let's allow larger variance for compression artifacts
    lo_diff = (40, 40, 40)
    up_diff = (40, 40, 40)
    
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    for seed in seeds:
        px = img[seed[1], seed[0]]
        print(f"Seed {seed} color: {px}")
        # Just floodfill. The tolerance handles the 'greenness'.
        cv2.floodFill(img, mask, seed, (0,0,0), lo_diff, up_diff, flood_flags)
    
    # Extract mask (remove border)
    # Mask has 255 for background, 0 for foreground
    bg_mask = mask[1:-1, 1:-1]
    
    # 3. Create Alpha Channel
    # background (255) -> alpha 0
    # foreground (0) -> alpha 255
    alpha = cv2.bitwise_not(bg_mask)
    
    # Clean up alpha (morphology)
    # Remove small noise holes
    # kernel = np.ones((3,3), np.uint8)
    # alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel) 
    
    # Soften edges
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    # Convert image to BGRA
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img_rgba[:, :, 3] = alpha

    # 4. Auto-Crop
    coords = cv2.findNonZero(alpha)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        print(f"Content bounds: x={x}, y={y}, w={w}, h={h}")
        
        # Add padding
        pad = 20
        h_img, w_img = img_rgba.shape[:2]
        
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w_img, x + w + pad)
        y2 = min(h_img, y + h + pad)
        
        cropped_img = img_rgba[y1:y2, x1:x2]
        print(f"Cropped from {w_img}x{h_img} to {x2-x1}x{y2-y1}")
        
        cv2.imwrite(output_path, cropped_img)
        print(f"Success! Saved to {output_path}")
    else:
        print("Error: No content found (alpha is all empty).")

process_monster_sprite("public/assets/ice_leviathan.png", "public/assets/ice_leviathan.png")
