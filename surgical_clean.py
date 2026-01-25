import cv2
import numpy as np

def surgical_manual_clean(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        a = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge([b, g, r, a])
    
    b, g, r, a = cv2.split(img)
    
    # 1. HARD WIPE SPECIFIC TROUBLE AREAS (Top right and sword interior regions)
    # The checkered sections shown in the screenshot:
    # Top-right quadrant
    # Around the character face/back hair (y: 100-300, x: 400-600)
    # Inside sword frame (y: 150-500, x: 600+)
    
    # Let's create a "Target Checker" mask by color and position
    is_neutral = (np.abs(r.astype(int) - g.astype(int)) < 25) & (np.abs(g.astype(int) - b.astype(int)) < 25)
    dark_check = (r < 70) & (g < 70) & (b < 70) & is_neutral
    gray_check = (r > 60) & (r < 165) & (g > 60) & (g < 165) & (b > 60) & (b < 165) & is_neutral
    
    checker_mask = dark_check | gray_check
    
    # 2. PROTECT THE VIBRANT STUFF
    # Character is mostly saturated REDS and ORANGES
    is_vibrant = (r > 120) & ( (r.astype(int) - g.astype(int)) > 30 )
    is_bright_yellow = (r > 200) & (g > 150)
    protection = is_vibrant | is_bright_yellow
    
    # Final cleanup mask: it looks like a checker AND it's not protected vibrant color
    final_bg = checker_mask & (~protection)
    
    # 3. Apply Alpha 0
    a[final_bg] = 0
    
    # 4. Surgical Diamond & Corner Wipe
    h, w = a.shape
    a[h-100:, w-100:] = 0 # Corner Diamond
    a[0:100, 0:100] = 0 # Top left
    a[0:150, w-200:] = 0 # Top right corner block
    
    # 5. Clean hair "floaties" - The hair area has some floating gray bits.
    # Wiping specific ROI to be absolute
    # y: 150-350, x: 480-600 roughly
    hair_roi_a = a[150:350, 480:600]
    hair_roi_checker = checker_mask[150:350, 480:600]
    hair_roi_a[hair_roi_checker] = 0
    
    # 6. Smooth the edges slightly
    # result = cv2.merge([b, g, r, a])
    # result = cv2.GaussianBlur(result, (3,3), 0) # No, keeps pixels crisp
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print("Surgical manual cleanup completed.")

surgical_manual_clean("public/assets/gemini_unit.png", "public/assets/gemini_unit_clean.png")
