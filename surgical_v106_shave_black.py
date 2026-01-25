import cv2
import numpy as np
import glob
import os

def surgical_v106_shave_black(output_path):
    # 1. Find the newest Gemini PNG (Look in parent dir too)
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None: return

    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    
    # 2. RAW EXTRACTION
    # Anything darker than average 40 is background.
    # This eats slightly deeper into the anti-aliased edge than V105 (which was < 30).
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 40  # (Avg ~13 per channel)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. BLACK SPILL REMOVAL (SHAVING)
    # The user sees a "Black Sticker" outline. We must shave it off.
    
    # Global Shave: 2px
    # This removes the black rim around the body/hydras.
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # 4. SPEAR EXTRA SHAVE
    # The spear outline often looks thicker. Let's hit it with +1px.
    h, w = alpha.shape
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.40)
    h_idx, w_idx = np.indices((h, w))
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    spear_part = np.zeros_like(alpha)
    spear_part[in_spear_box] = alpha[in_spear_box]
    spear_extra = cv2.erode(spear_part, kernel, iterations=1) # Total 3px for spear
    
    # Combine
    alpha[in_spear_box] = spear_extra[in_spear_box]
    
    # 5. CLEANUP
    # Remove top-left artifacts (if any, user saw a triangle)
    # Force opacity 0 in top-left corner (0-50px)
    alpha[0:50, 0:50] = 0
    
    # Apply
    rgba[:,:,3] = alpha
    rgba[alpha == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V106 Shave Complete: {output_path}")

surgical_v106_shave_black("public/assets/water_deity_unit_final.png")
