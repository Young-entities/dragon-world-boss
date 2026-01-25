import cv2
import numpy as np
import glob
import os

def surgical_v107_polish_black(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. RAW EXTRACTION
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. ORANGE AURA KILLER
    # User sees an "Orange Aura". This is the rust/dirt.
    # Logic: If Red is the dominant channel (Warm), it's not Ice. 
    # Exception: Skin is also Red dominant. We must PROTECT Skin.
    
    # Define Skin Zone (Center Column)
    col_x0, col_x1 = int(w*0.40), int(w*0.60)
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    # Identify "Orange/Warm" pixels
    is_warm = (r > b) & (r > g)
    
    # Nuke Weak Warm pixels that represent glow/aura
    # But ONLY outside the skin zone
    should_kill_orange = is_warm & (~in_skin_zone)
    
    alpha[should_kill_orange] = 0

    # 4. BLACK STICKER SHAVE (Aggressive)
    # Global Shave: 2px
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # 5. SPEAR SUPER SHAVE
    # Current: 2px global. Spear needs more.
    # Let's add 3px more (Total 5px).
    spear_y0, spear_y1 = int(h*0.55), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.45)
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    spear_part = np.zeros_like(alpha)
    spear_part[in_spear_box] = alpha[in_spear_box]
    # Erode 3 more times
    spear_extra = cv2.erode(spear_part, kernel, iterations=3) 
    alpha[in_spear_box] = spear_extra[in_spear_box]
    
    # 6. ARTIFACT CLEANUP
    alpha[0:50, 0:50] = 0
    
    # Save
    rgba[:,:,3] = alpha
    rgba[alpha == 0, :3] = 0
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V107 Polish Complete: {output_path}")

surgical_v107_polish_black("public/assets/water_deity_unit_final.png")
