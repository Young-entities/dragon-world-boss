
import cv2
import numpy as np

def restore_high_res_icons(input_path, out_dark_base, out_dark_circle, out_holy_base, out_holy_circle):
    print(f"Restoring High Res (128px) icons from: {input_path}")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Source Image not found")
        return

    h, w = img.shape[:2]
    mid_x = w // 2
    
    # Split
    img_dark = img[:, :mid_x]
    img_holy = img[:, mid_x:]
    
    TARGET_CANVAS = 128
    TARGET_RATIO = 0.94 # Matches Fire Circle
    
    def process_and_save(icon, path1, path2, name):
        # Convert BGRA
        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
        h, w = icon.shape[:2]
        
        # Remove White BG
        mask = np.zeros((h+2, w+2), np.uint8)
        seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1), (0, h//2), (w-1, h//2)] # More seeds
        lo = (15, 15, 15)
        up = (15, 15, 15)
        flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
        
        flooder = icon[:,:,:3].copy()
        for seed in seeds:
            cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
            
        bg_mask = mask[1:-1, 1:-1]
        icon[bg_mask > 0, 3] = 0
        
        # Crop Content
        a = icon[:, :, 3]
        contours, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return
            
        # Largest contour is the icon
        # Merge all significant contours?
        # Just use boundingRect of all non-zero alpha
        coords = cv2.findNonZero(a)
        x, y, cw, ch = cv2.boundingRect(coords)
        
        content = icon[y:y+ch, x:x+cw]
        
        # Resize to 128px target
        target_content_size = int(TARGET_CANVAS * TARGET_RATIO)
        # Use INTER_AREA if shrinking, INTER_CUBIC if growing
        # Source is 256px -> 120px (Shrink) -> Area
        new_content = cv2.resize(content, (target_content_size, target_content_size), interpolation=cv2.INTER_AREA)
        
        # Canvas
        new_img = np.zeros((TARGET_CANVAS, TARGET_CANVAS, 4), dtype=np.uint8)
        px = (TARGET_CANVAS - target_content_size) // 2
        py = (TARGET_CANVAS - target_content_size) // 2
        
        new_img[py:py+target_content_size, px:px+target_content_size] = new_content
        
        cv2.imwrite(path1, new_img)
        cv2.imwrite(path2, new_img)
        print(f"Saved High Res {name} to {path1} and {path2}")

    process_and_save(img_dark, out_dark_base, out_dark_circle, "Dark")
    process_and_save(img_holy, out_holy_base, out_holy_circle, "Holy")

src = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_icons_vector_1769750728695.png"

restore_high_res_icons(
    src,
    "public/assets/element_dark.png",
    "public/assets/element_dark_circle.png",
    "public/assets/element_holy.png",
    "public/assets/element_holy_circle.png"
)
