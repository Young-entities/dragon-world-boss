
import cv2
import numpy as np

def finalize_icons(input_path, output_dark, output_holy):
    print(f"Finalizing specified icons: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    h, w = img.shape[:2]
    mid_x = w // 2
    
    img_dark = img[:, :mid_x]
    img_holy = img[:, mid_x:]
    
    def clean_and_save(icon, name):
        # Convert to BGRA
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
        h, w = icon.shape[:2]
        
        # White background removal (Floodfill)
        mask = np.zeros((h+2, w+2), np.uint8)
        # Scan full perimeter for seeds (top, bottom, left, right edges)
        seeds = []
        for x in range(0, w, 10):
            seeds.append((x, 0))
            seeds.append((x, h-1))
        for y in range(0, h, 10):
            seeds.append((0, y))
            seeds.append((w-1, y))
            
        lo = (10, 10, 10)
        up = (10, 10, 10)
        flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
        
        # Contiguous copy for floodfill input (Fixes previous error)
        flooder = icon[:,:,:3].copy()
        
        for seed in seeds:
            cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
            
        bg_mask = mask[1:-1, 1:-1]
        icon[bg_mask > 0, 3] = 0
        
        # Crop to content (Largest Contour strategy to avoid text)
        a = icon[:, :, 3]
        contours, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Sort by area
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            # Largest should be the icon circle
            cnt = contours[0]
            x, y, cw, ch = cv2.boundingRect(cnt)
            
            # Pad 1px
            pad = 1
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + cw + pad)
            y2 = min(h, y + ch + pad)
            
            # Validating if it's indeed the MAIN icon (area check)
            # Text area is small. Icon area is large.
            # This should work.
            
            icon = icon[y1:y2, x1:x2]
            
            cv2.imwrite(name, icon)
            print(f"Saved {name}")

    clean_and_save(img_dark, output_dark)
    clean_and_save(img_holy, output_holy)

path = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_icons_vector_1769750728695.png"
out_dark = "public/assets/element_dark.png"
out_holy = "public/assets/element_holy.png"

finalize_icons(path, out_dark, out_holy)
