
import cv2
import numpy as np

def process_monster_perfect(input_path, output_path):
    print(f"Processing perfect transparency: {input_path}")
    
    img_bgr = cv2.imread(input_path)
    if img_bgr is None:
        print("Error: Image not found.")
        return

    h, w = img_bgr.shape[:2]

    # Floodfill on BGR image
    mask = np.zeros((h+2, w+2), np.uint8)
    # Seeds: corners and midpoints
    seeds = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1), (0, h//2), (w-1, h//2)]
    
    lo = (2, 2, 2)
    up = (2, 2, 2)
    flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    for seed in seeds:
        cv2.floodFill(img_bgr, mask, seed, (0,0,0), lo, up, flood_flags)
    
    bg_mask = mask[1:-1, 1:-1]
    
    # Convert to BGRA
    img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
    
    # Set Alpha to 0 where mask is set (255)
    img_bgra[bg_mask > 0, 3] = 0
    
    # Crop
    coords = cv2.findNonZero(cv2.bitwise_not(bg_mask))
    if coords is not None:
        x, y, w_rect, h_rect = cv2.boundingRect(coords)
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w, x + w_rect + pad)
        y2 = min(h, y + h_rect + pad)
        img_bgra = img_bgra[y1:y2, x1:x2]
        print(f"Cropped to {x2-x1}x{y2-y1}")

    cv2.imwrite(output_path, img_bgra)
    print(f"Saved to {output_path}")

original_path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/angel_lancer_no_fish_v1_1769739462457.png"
output_path = "public/assets/celestial_valkyrie.png"

process_monster_perfect(original_path, output_path)
