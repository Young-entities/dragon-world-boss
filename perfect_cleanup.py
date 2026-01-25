import cv2
import numpy as np

def perfect_cleanup(input_path, output_path):
    # Load the original raw gemini image
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
    
    # Ensure 4 channels
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape
    
    # 1. Target the Checkers by Neutrality
    # We use a threshold on the difference between channels
    r_int = r.astype(np.int16)
    g_int = g.astype(np.int16)
    b_int = b.astype(np.int16)
    
    diff_rg = np.abs(r_int - g_int)
    diff_gb = np.abs(g_int - b_int)
    is_neutral = (diff_rg < 10) & (diff_gb < 10)
    
    # Target specific checker luminosity
    v = np.max(img[:,:,:3], axis=2) 
    is_checker_v = (v < 50) | ((v > 85) & (v < 130))
    
    checker_candidate = is_neutral & is_checker_v
    
    # 2. SEED-BASED FLOOD FILL (To protect the character interior)
    # We only clear checkers that are connected to the boundary.
    # This prevents the script from clearing the character's face/interior
    # even if those parts are neutral gray.
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    combined = checker_candidate.astype(np.uint8) * 255
    
    # Seeds along edges
    for x in range(0, w, 20):
        if combined[0, x] == 255: cv2.floodFill(combined, flood_mask, (x, 0), 128)
        if combined[h-1, x] == 255: cv2.floodFill(combined, flood_mask, (x, h-1), 128)
    for y in range(0, h, 20):
        if combined[y, 0] == 255: cv2.floodFill(combined, flood_mask, (0, y), 128)
        if combined[y, w-1] == 255: cv2.floodFill(combined, flood_mask, (w-1, y), 128)
        
    actual_bg = (combined == 128)
    
    # 3. APPLY TRANSPARENCY
    a[actual_bg] = 0
    
    # CLEAR DIAMOND (Bottom Right)
    a[h-100:, w-100:] = 0
    
    # 4. FINAL SAVE
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Successful Surgical Cleanup: {output_path}")

perfect_cleanup("public/assets/gemini_unit.png", "public/assets/gemini_boss_final.png")
