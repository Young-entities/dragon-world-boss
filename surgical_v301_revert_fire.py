import cv2
import numpy as np
import glob
import os

def surgical_v301_revert_fire(output_path):
    # 1. FORCE SOURCE (Old Fire Unit)
    # The list showed this as a likely candidate from earlier today (00:49).
    target_file = "../Gemini_Generated_Image_ed2md4ed2md4ed2m.png"
    
    if not os.path.exists(target_file):
        print(f"Cannot find backup file: {target_file}")
        # Try finding ANY Gemini file that isn't the Screenshot
        files = glob.glob("../Gemini_*.png")
        # Filter out the Water Unit source if known? 
        # But Water Unit source was 'Screenshot...'.
        # So ANY Gemini file might be valid.
        files.sort(key=os.path.getmtime, reverse=True)
        # 16:43 file: 40sf...
        if files:
            target_file = files[0] # Pick newest Gemini
            print(f"Falling back to newest Gemini: {target_file}")
    
    print(f"Restoring Fire Unit from: {target_file}")
    
    img = cv2.imread(target_file)
    if img is None: return

    b, g, r = cv2.split(img)
    
    # 2. BLACK EXTRACTION (Assuming Fire Unit is Black BG)
    # Most prior Fire Units were Black BG.
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 50
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V301 Revert Fire Complete: {output_path}")

surgical_v301_revert_fire("public/assets/overlord_absolute_final.png")
