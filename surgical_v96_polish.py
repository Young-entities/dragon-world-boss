import cv2
import numpy as np

def surgical_v96_polish(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- RE-APPLY V95 LOGIC (Base) ---
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    is_bg_color = (luma > 210) & (saturation < 30)
    solid_matter = ~is_bg_color
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # Hole Fill
    pad = 10
    mask_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    h_pad, w_pad = mask_padded.shape
    flood_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(mask_padded, flood_mask, (0,0), 255)
    
    skeleton_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    ff_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(skeleton_padded, ff_mask, (0,0), 128)
    final_mask_padded = skeleton_padded.copy()
    final_mask_padded[skeleton_padded == 0] = 255
    final_mask_padded[skeleton_padded == 128] = 0
    final_mask = final_mask_padded[pad:-pad, pad:-pad]
    
    # Lake Draining
    potential_lakes = (final_mask == 255) & is_bg_color
    lake_labels_mask = np.zeros((h, w), dtype=np.uint8)
    lake_labels_mask[potential_lakes] = 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lake_labels_mask, 8, cv2.CV_32S)
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > 500: 
            final_mask[labels == i] = 0

    # --- V96 UPGRADES ---

    # 1. FACE RESCUE (Force Solid)
    # The geometric fill might have failed or the lake drain might have killed it.
    # We strictly enforce opacity on the face.
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    h_idx, w_idx = np.indices((h, w))
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    
    # Also enforce skin-tone solidity nearby
    is_skin = (r > g) & (g > b) & (r > 150)
    col_x0, col_x1 = int(w*0.40), int(w*0.60)
    in_body_col = (w_idx >= col_x0) & (w_idx <= col_x1)
    
    # Apply Face Rescue
    final_mask[in_face_box] = 255
    final_mask[in_body_col & is_skin] = 255

    # 2. RUST REMOVAL (Increased Erosion)
    # Erode the WHOLE unit by 2px (instead of 1px) to kill the orange glow halo.
    kernel = np.ones((2,2), np.uint8)
    final_mask = cv2.erode(final_mask, kernel, iterations=2)
    
    # 3. SPEAR PROTECTION (Don't erode the spear tip!)
    # We want the spear to remain sharp (from V90 logic), not blunted by the 2px erosion.
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.40)
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    # Re-apply the spear tip from the PRE-ERODED mask, but shave it separately?
    # Actually, the user liked V90 spear (3px shave).
    # Step: Let's apply V90 spear logic again on top.
    
    # Create the spear mask again from scratch logic? No, just use coordinates.
    # Recover pixels inside spear box from pre-erosion state
    # Wait, simple trick: Erode body 2px. Erode spear 3px.
    # Current 'final_mask' is eroded 2px globally.
    # The spear tip needs *more* shaving to avoid sticker (3px).
    # So we erode the spear area 1 more time.
    
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    spear_extra_shave = cv2.erode(spear_part, kernel, iterations=1) # 2+1=3 total
    
    # Update final mask with extra shaved spear
    final_mask[in_spear_box] = spear_extra_shave[in_spear_box]
    
    # Save
    rgba[:,:,3] = final_mask
    rgba[final_mask == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical Polish V96 COMPLETE: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v96_polish(source, "public/assets/water_deity_unit_final.png")
