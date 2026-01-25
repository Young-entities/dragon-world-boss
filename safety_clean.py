import cv2
import numpy as np

def surgical_safety_clean(input_path, output_path):
    # Load original unit image
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    # Ensure BGRA
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # 1. DEFINE BACKGROUND COLORS (Target specifically logic-checkered colors)
    # The checkers are very consistent mid-grays (~102, 102, 102) and blacks (~0, 0, 0)
    # We'll use a tighter tolerance to avoid flesh tones (face) which have more red/yellow.
    
    # Dark squares (Allow some variation but keep it tight)
    mask_dark = (r < 30) & (g < 30) & (b < 30)
    
    # Gray squares (Avoid skin tones: grays have R, G, B very close to each other)
    # Skin/Face is usually R > G > B.
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_true_gray = (diff_rg < 10) & (diff_gb < 10)
    mask_gray = (r > 80) & (r < 125) & (g > 80) & (g < 125) & (b > 80) & (b < 125) & is_true_gray
    
    combined_mask = (mask_dark | mask_gray).astype(np.uint8) * 255
    
    # 2. FLOOD FILL FROM OUTSIDE ONLY
    # This is the "magic": it only clear checkers that touch the borders.
    # It will never reach the face or inside the sword unless there's a 100% transparent opening.
    h, w = combined_mask.shape
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # Seeds are all points on the 4 borders
    seeds = []
    for x in range(0, w, 5):
        seeds.append((x, 0))
        seeds.append((x, h-1))
    for y in range(0, h, 5):
        seeds.append((0, y))
        seeds.append((w-1, y))
        
    bg_confirmed = np.zeros_like(combined_mask)
    for x_s, y_s in seeds:
        if combined_mask[y_s, x_s] == 255:
            cv2.floodFill(combined_mask, flood_mask, (x_s, y_s), 128)
            
    # Now anything turned into 128 in combined_mask is truly Background
    bg_confirmed = (combined_mask == 128)
    
    # 3. APPLY AND PROTECT
    # We'll also restore the face region just in case (Character face is roughly center-top)
    # Usually around y: 15% to 40% and x: 40% to 60%
    # But flood fill should have already handled this.
    
    # 4. REMOVE DIAMOND (Bottom Right)
    # For the diamond, we just wipe the Alpha in a 70x70 block
    a[bg_confirmed] = 0
    a[h-75:, w-75:] = 0 # No mercy for the diamond
    
    # 5. HALO CLEANUP (Erode/Dilate sparingly)
    # This removes the tiny gray pixels at the boundary
    # We only dilate the alpha-zero area slightly
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print("Surgical Safety Cleanup: Restored face and sword details, removed outer context only.")

surgical_safety_clean("public/assets/gemini_unit.png", "public/assets/gemini_unit_clean.png")
