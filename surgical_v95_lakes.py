import cv2
import numpy as np

def surgical_v95_lakes(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- RE-APPLY V90 LOGIC (Base: Solid Unit + Destickered Edges) ---
    # We must rebuild the solid mask first.
    
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    is_bg_color = (luma > 210) & (saturation < 30)
    solid_matter = ~is_bg_color
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # Hole Fill (Flood Fill from Outside)
    pad = 10
    mask_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    h_pad, w_pad = mask_padded.shape
    flood_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(mask_padded, flood_mask, (0,0), 255)
    
    # Invert trick to get filled holes
    skeleton_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    ff_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(skeleton_padded, ff_mask, (0,0), 128)
    final_mask_padded = skeleton_padded.copy()
    final_mask_padded[skeleton_padded == 0] = 255
    final_mask_padded[skeleton_padded == 128] = 0
    final_mask = final_mask_padded[pad:-pad, pad:-pad]
    
    # --- V95 UPGRADE: LAKE DRAINING ---
    # The problem: Trapped white regions were "filled" by the flood fill because they were enclosed.
    # We need to detect these pockets inside 'final_mask' and kill them if they are just white background.
    
    # logic: Scan pixels that are currently marked "Solid" (255) BUT are actually "Background Color".
    # These are the "Filled Lakes" (and also the face/spear highlights).
    
    potential_lakes = (final_mask == 255) & is_bg_color
    
    # Convert to blob analysis
    lake_labels_mask = np.zeros((h, w), dtype=np.uint8)
    lake_labels_mask[potential_lakes] = 255
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lake_labels_mask, 8, cv2.CV_32S)
    
    # Threshold: If a white blob is huge (> 500px), it's a Background Lake. Kill it.
    # If it's small (< 500px), it's a detail (Eye/Spear). Keep it.
    
    kills = 0
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        
        if area > 500: # Threshold for "Lake" vs "Highlight"
            # Dig a hole in the final mask
            final_mask[labels == i] = 0
            kills += 1
            
    print(f"Drained {kills} trapped background lakes.")

    # --- EDGE TRIMMER (V90 Logic) ---
    kernel = np.ones((2,2), np.uint8)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    
    # Spear Shave
    spear_y0, spear_y1 = int(h*0.50), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.50)
    h_idx, w_idx = np.indices((h, w))
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    feature_mask = final_mask.copy()
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    spear_shaved = cv2.erode(spear_part, kernel, iterations=2) # 3px total
    
    body_part = final_mask.copy()
    body_part[in_spear_box] = 0
    combined_mask = cv2.bitwise_or(body_part, spear_shaved)
    
    # Save
    rgba[:,:,3] = combined_mask
    rgba[combined_mask == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V95 COMPLETE: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v95_lakes(source, "public/assets/water_deity_unit_final.png")
