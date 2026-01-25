import cv2
import numpy as np

def nuclear_transparency(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    if img.shape[2] == 3: img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # Target EVERY white pixel (even off-white)
    # If all three channels are very high, it is background.
    is_white = (r > 200) & (g > 200) & (b > 200)
    
    # Also target "Neutral" pixels (R=G=B) that are bright
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_neutral = (diff_rg < 20) & (diff_gb < 20) & (r > 150)
    
    # Combined mask
    bg_mask = is_white | is_neutral
    
    # Kill the alpha for all of them
    a[bg_mask] = 0
    
    # Squeeze the edges by 1px to ensure no white line remains
    kernel = np.ones((3,3), np.uint8)
    a = cv2.erode(a, kernel, iterations=1)
    
    # Nuke the corner watermark area just in case
    h, w = a.shape
    a[h-100:, w-100:] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print("Nuclear transparency applied: All white and bright-gray nuked.")

nuclear_transparency("public/assets/overlord_white_bg.png", "public/assets/overlord_perfect_v2.png")
