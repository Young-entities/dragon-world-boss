
import cv2
import numpy as np

def process_icons(input_path, output_dark, output_holy):
    print(f"Processing icons from: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        return

    h, w = img.shape[:2]
    mid_x = w // 2
    
    # Split
    img_dark = img[:, :mid_x]
    img_holy = img[:, mid_x:]
    
    # Function to process single icon
    def clean_icon(icon_img, name):
        # Convert to BGRA
        icon_bgra = cv2.cvtColor(icon_img, cv2.COLOR_BGR2BGRA)
        h, w = icon_bgra.shape[:2]
        
        # Floodfill black background
        # Seed points: corners
        mask = np.zeros((h+2, w+2), np.uint8)
        seeds = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
        
        # Tolerance: Black is (0,0,0). But jpeg artifacts might be (5,5,5).
        lo = (10, 10, 10)
        up = (10, 10, 10)
        flood_flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
        
        for seed in seeds:
            cv2.floodFill(icon_bgra[:,:,:3], mask, seed, (0,0,0), lo, up, flood_flags)
        
        bg_mask = mask[1:-1, 1:-1]
        
        # Set Alpha to 0
        icon_bgra[bg_mask > 0, 3] = 0
        
        # Crop to content
        coords = cv2.findNonZero(icon_bgra[:, :, 3])
        if coords is not None:
            x, y, cw, ch = cv2.boundingRect(coords)
            pad = 2
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + cw + pad)
            y2 = min(h, y + ch + pad)
            icon_bgra = icon_bgra[y1:y2, x1:x2]
        
        # Resize to standard size? E.g. 64x64 or 128x128
        # Let's keep resolution high (~200px?) for quality.
        cv2.imwrite(name, icon_bgra)
        print(f"Saved {name}")

    clean_icon(img_dark, output_dark)
    clean_icon(img_holy, output_holy)

path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_icons_dark_holy_1769750592634.png"
out_dark = "public/assets/element_dark.png"
out_holy = "public/assets/element_holy.png"

process_icons(path, out_dark, out_holy)
