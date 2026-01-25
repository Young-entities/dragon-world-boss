import cv2
import numpy as np

def remove_diamond_v3(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape
    
    # 1. Target the Diamond by color and position
    # The diamond is usually a light gray/white sparkle.
    # We will target neutral colors (R~G~B) that are bright.
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_neutral = (diff_rg < 10) & (diff_gb < 10)
    is_bright = (r > 160) & (g > 160) & (b > 160)
    
    # The diamond is almost always in the bottom-right quadrant
    # specifically the bottom 25% and right 25%
    roi_mask = np.zeros_like(a, dtype=bool)
    roi_mask[int(h*0.75):, int(w*0.75):] = True
    
    diamond_mask = is_neutral & is_bright & roi_mask
    
    # Wipe the diamond
    a[diamond_mask] = 0
    
    # 2. Hard wipe a larger corner just in case it's more "into" the corner
    # Some AI marks are right at the very edge.
    a[h-120:, w-120:] = 0
    
    # 3. Clean up the white background (as before)
    # Target pure white areas
    is_white_bg = (r > 240) & (g > 240) & (b > 240)
    a[is_white_bg] = 0
    
    # 4. Refine edges to remove the "white line"
    kernel = np.ones((3,3), np.uint8)
    char_mask = (a > 0).astype(np.uint8) * 255
    char_mask_eroded = cv2.erode(char_mask, kernel, iterations=1)
    a[char_mask_eroded == 0] = 0
    
    # Slight blur on alpha for smoothness
    a = cv2.GaussianBlur(a, (3,3), 0)
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Diamond removal V3 completed: {output_path}")

remove_diamond_v3("public/assets/overlord_white_bg.png", "public/assets/overlord_no_diamond.png")
