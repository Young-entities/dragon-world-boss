
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

    # 2. Floodfill green background
    seeds = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Larger tolerance just in case
    lo_diff = (40, 40, 40)
    up_diff = (40, 40, 40)
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    for seed in seeds:
        cv2.floodFill(img, mask, seed, (0,0,0), lo_diff, up_diff, flood_flags)
    
    bg_mask = mask[1:-1, 1:-1]
    alpha = cv2.bitwise_not(bg_mask)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)

    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img_rgba[:, :, 3] = alpha

    # 3. Auto-Crop
    coords = cv2.findNonZero(alpha)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        
        # Padding
        pad = 20
        h_img, w_img = img_rgba.shape[:2]
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w_img, x + w + pad)
        y2 = min(h_img, y + h + pad)
        
        cropped_img = img_rgba[y1:y2, x1:x2]
        cv2.imwrite(output_path, cropped_img)
        print(f"Success! Saved to {output_path} (Cropped: {x2-x1}x{y2-y1})")
    else:
        print("Error: No content found.")

process_monster_sprite("public/assets/celestial_valkyrie.png", "public/assets/celestial_valkyrie.png")
