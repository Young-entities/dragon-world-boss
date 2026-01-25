import cv2
import numpy as np

def surgical_v97_neck(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- RE-APPLY V96 LOGIC (Base) ---
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    is_bg_color = (luma > 210) & (saturation < 30)
    solid_matter = ~is_bg_color
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # Hole Fill (Geometric Solidity)
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
    
    # --- V97 UPGRADE: SMART LAKE DRAINING ---
    potential_lakes = (final_mask == 255) & is_bg_color
    lake_labels_mask = np.zeros((h, w), dtype=np.uint8)
    lake_labels_mask[potential_lakes] = 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lake_labels_mask, 8, cv2.CV_32S)
    
    # Define "Neck Zone" (Upper area where small white chunks exist)
    # y: 0 to 50%, x: 20% to 80%
    neck_y0, neck_y1 = 0, int(h * 0.5)
    neck_x0, neck_x1 = int(w * 0.2), int(w * 0.8)

    kills = 0
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids[i][0]), int(centroids[i][1])
        
        # Rule 1: Kill Huge Lakes (> 500px) anywhere (Background)
        should_kill = False
        if area > 500:
            should_kill = True
            
        # Rule 2: Kill Small Lakes (> 50px) if they are in the Neck Zone
        # This catches the white chunk behind her hair.
        # It won't kill the Spear Tip (because spear is in bottom half).
        # It MIGHT kill the Eye Highlights, BUT... Face Rescue will save them later.
        in_neck_zone = (neck_y0 <= cy <= neck_y1) and (neck_x0 <= cx <= neck_x1)
        if area > 50 and in_neck_zone:
            should_kill = True
            
        if should_kill:
            final_mask[labels == i] = 0
            kills += 1

    # --- FACE RESCUE (Force Solid) ---
    # This brings back eyes if we accidentally drained them
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    h_idx, w_idx = np.indices((h, w))
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    
    is_skin = (r > g) & (g > b) & (r > 150)
    col_x0, col_x1 = int(w*0.40), int(w*0.60)
    in_body_col = (w_idx >= col_x0) & (w_idx <= col_x1)
    
    final_mask[in_face_box] = 255
    final_mask[in_body_col & is_skin] = 255

    # --- RUST & STICKER REMOVAL (V96) ---
    # Global 2px erode
    kernel = np.ones((2,2), np.uint8)
    final_mask = cv2.erode(final_mask, kernel, iterations=2)
    
    # Spear 3px shave (re-apply on top)
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.40)
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    spear_extra_shave = cv2.erode(spear_part, kernel, iterations=1) # Total 3px
    final_mask[in_spear_box] = spear_extra_shave[in_spear_box]
    
    # Save
    rgba[:,:,3] = final_mask
    rgba[final_mask == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical Polish V97 COMPLETE: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v97_neck(source, "public/assets/water_deity_unit_final.png")
