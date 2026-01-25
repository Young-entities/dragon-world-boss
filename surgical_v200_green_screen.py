import cv2
import numpy as np
import glob
import os

def surgical_v200_green_screen(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    
    # 2. GREEN SCREEN EXTRACTION
    # Green is Dominant and Bright
    # G > R + 20 and G > B + 20 and G > 100
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # 3. ANTI-SPILL (De-Green)
    # Removing green reflection from the edges of the ice.
    # Logic: Green channel shouldn't exceed the average of R and B?
    # Or simple "min(G, B)"? Ice is Blue/Cyan (High G, High B).
    # If G > B, it's teal/greenish.
    # Let's effectively "Kill Green Halo" by clamping G to B if it's very green?
    # Actually, standard Despill: G = min(G, max(R, B))
    
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb) 
    # This turns Pure Green (0,255,0) into Black (0,0,0).
    # This turns Yellow (255,255,0) into Red (255,0,0).
    # This turns Cyan (0,255,255) into Cyan (0,255,255) -- SAFE for Ice!
    
    # 4. ORANGE KILLER (Nuclear Winter Lite)
    # Just to be safe and clean the rust.
    # R <= B
    h, w = img.shape[:2]
    # Protect Skin
    col_x0, col_x1 = int(w*0.43), int(w*0.57) 
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)

    # 5. BLACK OUTLINE CHECK
    # Does the green screen version have the black outline?
    # Usually NO, because the AI draws lighter edges on bright backgrounds.
    # But if it does, we can try to lighten it.
    # Let's apply a subtle "Shadow Lift" just in case.
    # If pixel is Black/Dark, make it Dark Blue.
    brightness = new_r.astype(int) + new_g.astype(int) + b.astype(int)
    is_very_dark = (brightness < 60) & (alpha == 255)
    new_b_out = b.copy()
    new_b_out[is_very_dark] = 100 # Safety Blue

    # 6. SHAVE (1px Clean)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([new_b_out, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V200 Green Screen Complete: {output_path}")

surgical_v200_green_screen("public/assets/water_deity_unit_final.png")
