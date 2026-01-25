import cv2
import numpy as np

def surgical_v101_restore(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None: return

    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- 1. RESTORE ROBUST BASE (From V96) ---
    # Background: Bright (>210) AND Low Sat (<30).
    # This was the stable setting before the V100 disaster.
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    is_bg_color = (luma > 210) & (saturation < 30)
    solid_matter = ~is_bg_color
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # SAFETY: Dilate the solid matter slightly to close gaps in Hydras
    # This prevents the flood fill from leaking inside and nuking the unit.
    kernel = np.ones((2,2), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    # --- 2. HOLE FILL ---
    pad = 10
    mask_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    h_pad, w_pad = mask_padded.shape
    
    # Flood Fill Background (128)
    skeleton_padded = mask_padded.copy()
    ff_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(skeleton_padded, ff_mask, (0,0), 128)
    
    # Recover Unit
    final_mask_padded = np.zeros_like(skeleton_padded)
    # Keep Original Solid (255) AND Filled Holes (0 -> 255)
    # Background is (128) -> 0
    final_mask_padded[skeleton_padded != 128] = 255
    
    final_mask = final_mask_padded[pad:-pad, pad:-pad]
    
    # Erode back 1px (undo the safety dilation)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)

    # --- 3. LAKE DRAIN (V97 Logic) ---
    potential_lakes = (final_mask == 255) & is_bg_color
    lake_labels_mask = np.zeros((h, w), dtype=np.uint8)
    lake_labels_mask[potential_lakes] = 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lake_labels_mask, 8, cv2.CV_32S)
    
    neck_y0, neck_y1 = 0, int(h * 0.5)
    neck_x0, neck_x1 = int(w * 0.2), int(w * 0.8)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids[i][0]), int(centroids[i][1])
        should_kill = False
        if area > 500: should_kill = True # Big lakes
        # Small lakes in neck zone
        if area > 50 and (neck_y0 <= cy <= neck_y1) and (neck_x0 <= cx <= neck_x1):
             should_kill = True
        if should_kill:
            final_mask[labels == i] = 0

    # --- 4. MANUAL ERASER (The Stubborn Chunk) ---
    # Safe box behind neck.
    eraser_y0, eraser_y1 = int(h*0.28), int(h*0.40)
    eraser_x0, eraser_x1 = int(w*0.35), int(w*0.41)
    h_idx, w_idx = np.indices((h, w))
    in_eraser_box = (h_idx >= eraser_y0) & (h_idx <= eraser_y1) & (w_idx >= eraser_x0) & (w_idx <= eraser_x1)
    
    is_bright = luma > 180
    final_mask[in_eraser_box & is_bright] = 0

    # --- 5. FINISH POLISH ---
    # Face Rescue
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    final_mask[in_face_box] = 255

    # Rust Remove (1px only - conservative)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    
    # Spear Shave (3px)
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.40)
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    spear_extra_shave = cv2.erode(spear_part, kernel, iterations=2) 
    final_mask[in_spear_box] = spear_extra_shave[in_spear_box]
    
    rgba[:,:,3] = final_mask
    rgba[final_mask == 0, :3] = 0
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V101 RESTORED: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v101_restore(source, "public/assets/water_deity_unit_final.png")
