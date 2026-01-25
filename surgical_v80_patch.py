import cv2
import numpy as np

def surgical_v80_patch(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- BASE LOGIC (V71 - The one that cleaned the background well) ---
    # Brightness + Low Saturation = Background
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    # Thresholds
    is_bg = (luma > 220) & (saturation < 20)
    
    # Initial mask
    alpha = np.ones_like(luma, dtype=np.uint8) * 255
    alpha[is_bg] = 0

    # --- PATCH 1: FACE & SKIN (Force Solid) ---
    # Face Box (Widened slightly)
    face_y0, face_y1 = int(h*0.18), int(h*0.38)
    face_x0, face_x1 = int(w*0.40), int(w*0.60)
    
    # Body Column (For skin protection)
    col_x0, col_x1 = int(w*0.35), int(w*0.65)
    
    h_idx, w_idx = np.indices((h, w))
    
    # Masks
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    in_body_col = (w_idx >= col_x0) & (w_idx <= col_x1)
    
    # Skin color logic (Warm tones)
    is_skin = (r > g) & (g > b) & (r > 150)
    
    # Apply Face/Skin Patches
    alpha[in_face_box] = 255  # Face is 100% solid, period.
    alpha[in_body_col & is_skin] = 255 # Skin in center is solid.

    # --- PATCH 2: WEAPON (Ice Preservation) ---
    # Spear is in bottom-left quadrant.
    spear_y0, spear_y1 = int(h*0.50), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.50)
    
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    # Ice Logic: Ice is BLUE. Background is Neutral.
    # If Blue is even slightly higher than Red, it's likely Ice/Shadow, not Background.
    # Background white/grey usually has R channel >= B channel (warm white/grey).
    is_ice = (b > r)
    
    # Apply Spear Patch
    # If inside spear box AND it looks like ice, Force Solid.
    alpha[in_spear_box & is_ice] = 255

    # --- FINISHING ---
    # Smart Edge Cleaning
    # We want to erode edge noise, BUT NOT the sharp spear tip or face details.
    
    # Create a "Do Not Erode" mask (Face + Spear Tip)
    safe_zone = in_face_box | (in_spear_box & is_ice)
    
    # Erode everywhere
    kernel = np.ones((2,2), np.uint8) # Gentle 1px erosion
    alpha_eroded = cv2.erode(alpha, kernel, iterations=1)
    
    # Put back the safe zones (restore them to full original alpha)
    # This prevents the spear tip from getting shaved off.
    alpha_final = np.where(safe_zone, alpha, alpha_eroded)
    
    rgba[:,:,3] = alpha_final
    
    # Cleanup ghost colors
    rgba[alpha_final == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical Patch V80 Complete: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v80_patch(source, "public/assets/water_deity_unit_final.png")
