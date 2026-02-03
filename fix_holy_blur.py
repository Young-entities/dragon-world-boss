
import cv2
import numpy as np

def fix_holy_blur(input_path, output_base, output_circle):
    print("Fixing Holy blur by creating a clean 128px version (Sweet Spot Resolution)...")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Source not found")
        return

    h, w = img.shape[:2]
    mid_x = w // 2
    
    # Holy is Right Side
    # But wait, original 'cut_exact_icons' split by mid_x.
    # Dark Left, Holy Right.
    icon = img[:, mid_x:]
    
    # Process
    icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
    h, w = icon.shape[:2]
    
    # Floodfill BG
    mask = np.zeros((h+2, w+2), np.uint8)
    seeds = [(0,0), (0, h-1), (w-1, 0), (w-1, h-1)]
    lo = (20, 20, 20)
    up = (20, 20, 20)
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    flooder = icon[:,:,:3].copy()
    for seed in seeds:
        cv2.floodFill(flooder, mask, seed, (255,255,255), lo, up, flags)
    
    bg_mask = mask[1:-1, 1:-1]
    icon[bg_mask > 0, 3] = 0
    
    # Find Contour (Robust Crop)
    a = icon[:, :, 3]
    contours, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No contours found")
        return
        
    cnt = max(contours, key=cv2.contourArea)
    x, y, cw, ch = cv2.boundingRect(cnt)
    
    content = icon[y:y+ch, x:x+cw]
    
    # Resize to 120px (Fits in 128px with 0.94 ratio)
    TARGET_SIZE = 120
    CANVAS_SIZE = 128
    
    # High Quality Downscale
    new_content = cv2.resize(content, (TARGET_SIZE, TARGET_SIZE), interpolation=cv2.INTER_AREA)
    
    new_img = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.uint8)
    px = (CANVAS_SIZE - TARGET_SIZE) // 2
    py = (CANVAS_SIZE - TARGET_SIZE) // 2
    
    new_img[py:py+TARGET_SIZE, px:px+TARGET_SIZE] = new_content
    
    cv2.imwrite(output_base, new_img)
    cv2.imwrite(output_circle, new_img)
    print(f"Saved optimized 128px Holy Icon to {output_base}")

src = r"C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/element_icons_vector_1769750728695.png"

fix_holy_blur(
    src,
    "public/assets/element_holy.png",
    "public/assets/element_holy_circle.png"
)
