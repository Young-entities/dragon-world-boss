
import cv2
import numpy as np

def process_vector_icons(input_path, output_dark, output_holy):
    print(f"Processing vector icons: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        return

    h, w = img.shape[:2]
    mid_x = w // 2
    
    img_dark = img[:, :mid_x]
    img_holy = img[:, mid_x:]
    
    def clean_and_save(icon, name):
        # Convert to BGRA
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
        h, w = icon.shape[:2]
        
        mask = np.zeros((h+2, w+2), np.uint8)
        seeds = [(0, 0), (0, h-1), (w-1, 0), (w-1, h-1), (w//2, 0), (w//2, h-1)] 
        # Added midpoints just in case
        
        lo = (10, 10, 10)
        up = (10, 10, 10)
        flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
        
        # FIX: Create contiguous copy for floodfill input
        flooder = icon[:,:,:3].copy()
        
        for seed in seeds:
            cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
            
        bg_mask = mask[1:-1, 1:-1]
        icon[bg_mask > 0, 3] = 0
        
        # Crop to content (Largest Contour strategy)
        a = icon[:, :, 3]
        contours, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cnt = contours[0]
            x, y, cw, ch = cv2.boundingRect(cnt)
            
            # Pad 2px
            pad = 2
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + cw + pad)
            y2 = min(h, y + ch + pad)
            
            icon = icon[y1:y2, x1:x2]
            
            cv2.imwrite(name, icon)
            print(f"Saved {name}")

    clean_and_save(img_dark, output_dark)
    clean_and_save(img_holy, output_holy)

path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_icons_vector_1769750728695.png"
out_dark = "public/assets/element_dark.png"
out_holy = "public/assets/element_holy.png"

process_vector_icons(path, out_dark, out_holy)
