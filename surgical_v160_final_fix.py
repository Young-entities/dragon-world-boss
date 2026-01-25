import cv2
import numpy as np
import glob
import os

def surgical_v160_final_fix(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. RAW EXTRACTION
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. BLACK STICKER REMOVAL (Saturation Filter)
    # Diagnosis confirmed outline pixels have Saturation ~11.
    # We delete anything Low-Sat and Dark.
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    luma = 0.299*r + 0.587*g + 0.114*b
    
    # Filter 1: Outline is Neutral-ish (Sat < 25) and Dark-ish (Luma < 60)
    is_sticker = (saturation < 25) & (luma < 60)
    
    # PROTECT FACE (Eyes/Lashes are also black/neutral)
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    h_idx, w_idx = np.indices((h, w))
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    
    # Apply Sticker Removal (Outside Face)
    alpha[is_sticker & (~in_face_box)] = 0
    
    # 4. AURA REMOVAL (Nuclear Winter)
    # Force Cool Colors outside Skin Zone.
    
    col_x0, col_x1 = int(w*0.43), int(w*0.57)
    col_y0, col_y1 = int(h*0.20), int(h*0.60)
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    outside_skin = ~in_skin_zone
    current_r = r[outside_skin]
    current_g = g[outside_skin]
    current_b = b[outside_skin]

    # Math: Clamp Red to Low Level (Blue). Kills Orange.
    new_r = r.copy()
    new_r[outside_skin] = np.minimum(current_r, current_b)
    
    # Math: Clamp Green too. Kills Yellow/Mud.
    # Allow Green to be slightly higher than Blue (Teal is ok), but not Yellow (R+G).
    new_g = g.copy()
    new_g[outside_skin] = np.minimum(current_g, current_b + 40)
    
    # 5. ARTIFACT CLEANUP
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([b, new_g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V160 Final Fix Complete: {output_path}")

surgical_v160_final_fix("public/assets/water_deity_unit_final.png")
