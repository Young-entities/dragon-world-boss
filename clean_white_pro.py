import cv2
import numpy as np

def nuclear_white_wipe_v2(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape
    
    # 1. Target white background
    is_white = (r > 235) & (g > 235) & (b > 235)
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_neutral = (diff_rg < 15) & (diff_gb < 15)
    
    bg_mask = is_white & is_neutral
    a[bg_mask] = 0
    
    # 2. SPECIFICALLY REMOVE DIAMOND (Watermark)
    # The diamond is in the bottom right corner area.
    # We will wipe a 100x100 block in the bottom right corner.
    a[h-100:, w-100:] = 0
    
    # 3. Clean up the edges
    kernel = np.ones((3,3), np.uint8)
    char_mask = (a > 0).astype(np.uint8) * 255
    char_mask_eroded = cv2.erode(char_mask, kernel, iterations=1)
    a[char_mask_eroded == 0] = 0
    
    # Gaussian blur for smoothing edges
    a = cv2.GaussianBlur(a, (3,3), 0)
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Cleanup with watermark removal completed: {output_path}")

# Run on the source white-background image again
nuclear_white_wipe_v2("public/assets/overlord_white_bg.png", "public/assets/overlord_final_pro.png")
