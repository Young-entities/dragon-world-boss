import cv2
import numpy as np

def surgical_v100_solidify(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None: return

    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- 1. BASE LOGIC (Relaxed to save Hydras/Puddle) ---
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    # RELAXED Threshold: Sat < 15 (was 30). 
    # This prevents killing pale blue ice/puddle.
    is_bg_color = (luma > 215) & (saturation < 15)
    solid_matter = ~is_bg_color
    
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # --- 2. HOLE FILL (Solidify Unit) ---
    pad = 10
    mask_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    h_pad, w_pad = mask_padded.shape
    flood_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    # Fill from outside (defines the ocean)
    cv2.floodFill(mask_padded, flood_mask, (0,0), 255)
    
    # Invert to get the solid unit
    # Everything NOT 255 is the unit (including internal holes)
    final_mask_padded = np.zeros_like(mask_padded)
    final_mask_padded[mask_padded == 0] = 255 # Unit + Holes
    
    # Crop back
    final_mask = final_mask_padded[pad:-pad, pad:-pad]
    
    # --- 3. LAKE DRAIN (Large Pockets) ---
    # Since we relaxed saturation, more background lakes might survive.
    # We must drain them.
    # Re-calc "is_bg_color" with the stricter V90 threshold just for lake detection?
    # No, stick to the V100 threshold but be aggressive only in huge areas.
    
    # Identify White Lakes inside the Solid Unit
    # Note: final_mask is the geometric solid. We look for pixels inside it that look like background.
    potential_lakes = (final_mask == 255) & is_bg_color
    lake_mask = np.zeros((h, w), dtype=np.uint8)
    lake_mask[potential_lakes] = 255
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lake_mask, 8, cv2.CV_32S)
     
    # Iterate lakes
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        
        # Determine if it's a Lake or a Detail
        should_kill = False
        
        # Kill Huge Lakes > 500px anywhere
        if area > 500: should_kill = True
        
        # Kill Medium Lakes > 50px in the Head Zone
        cx, cy = int(centroids[i][0]), int(centroids[i][1])
        if area > 50 and (cy < h*0.5) and (cx > w*0.2) and (cx < w*0.8):
             should_kill = True
             
        if should_kill:
            final_mask[labels == i] = 0

    # --- 4. NEUTRAL NUKE (The Stubborn Chunk) ---
    # Refined Zone and Threshold
    eraser_y0, eraser_y1 = int(h*0.20), int(h*0.55)
    eraser_x0, eraser_x1 = int(w*0.25), int(w*0.48)
    h_idx, w_idx = np.indices((h, w))
    in_eraser_box = (h_idx >= eraser_y0) & (h_idx <= eraser_y1) & (w_idx >= eraser_x0) & (w_idx <= eraser_x1)
    
    # Stricter Neutrality: B - R < 15. Catches slightly blue-ish white.
    is_neutral = (b.astype(int) - r.astype(int)) < 15
    is_bright = luma > 180
    
    # Only nuke if Bright + Neutral
    final_mask[in_eraser_box & is_neutral & is_bright] = 0

    # --- 5. POLISH & RESCUE ---
    
    # Face & Skin Rescue (Crucial after Nuke)
    face_y0, face_y1 = int(h*0.20), int(h*0.35)
    face_x0, face_x1 = int(w*0.42), int(w*0.58)
    in_face_box = (h_idx >= face_y0) & (h_idx <= face_y1) & (w_idx >= face_x0) & (w_idx <= face_x1)
    
    is_skin = (r > g) & (g > b) & (r > 150)
    col_x0, col_x1 = int(w*0.40), int(w*0.60)
    in_body_col = (w_idx >= col_x0) & (w_idx <= col_x1)

    final_mask[in_face_box] = 255
    final_mask[in_body_col & is_skin] = 255

    # 1px Erode (Rust Removal - Reduced from 2px to save Hydras)
    # User said Hydras were "transparent" (maybe thin?). 1px is safer.
    kernel = np.ones((2,2), np.uint8)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    
    # Spear Shave (3px - Kept for sticker removal)
    spear_y0, spear_y1 = int(h*0.60), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.40)
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    spear_extra_shave = cv2.erode(spear_part, kernel, iterations=2) # 1+2=3 total
    final_mask[in_spear_box] = spear_extra_shave[in_spear_box]
    
    # Save
    rgba[:,:,3] = final_mask
    rgba[final_mask == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V100 COMPLETE: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v100_solidify(source, "public/assets/water_deity_unit_final.png")
