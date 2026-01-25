import cv2
import numpy as np
import glob
import os

def surgical_v213_edge_save(output_path):
    # 1. Source (Screenshot)
    search_pattern = "../*.png"
    files = glob.glob(search_pattern)
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. GREEN EXTRACTION
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # 3. MINIMAL CROP (The Fix)
    # V212 cropped 15% which decapitated the spear.
    # We only need to remove the "Artifact Line" on the edge.
    # 20 pixels (approx 3%) should correspond to the artifact without hitting the spear.
    crop_pixels = 20
    alpha[:, :crop_pixels] = 0
    alpha[:, -crop_pixels:] = 0 # Right side too just in case
    
    # 4. DESPILL
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb)
    
    # 5. ORANGE KILLER
    col_x0, col_x1 = int(w*0.43), int(w*0.57) 
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)

    # 6. SHADOW LIFT
    brightness = new_r.astype(int) + new_g.astype(int) + b.astype(int)
    is_very_dark = (brightness < 60) & (alpha == 255)
    new_b_out = b.copy()
    new_b_out[is_very_dark] = 100 
    
    # 7. SHAVE
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([new_b_out, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V213 Edge Save Complete: {output_path}")

surgical_v213_edge_save("public/assets/water_deity_unit_final.png")
