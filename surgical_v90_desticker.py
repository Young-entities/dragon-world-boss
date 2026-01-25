import cv2
import numpy as np

def surgical_v90_desticker(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    # --- GEOMETRIC SOLIDITY (Fixes Snakes/Face Transparency) ---
    
    # Define "Unit Material" (Everything that ISN'T background)
    # Background is Bright (>210) AND Neutral (Sat < 20).
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    # Identify the background pixels
    is_bg_color = (luma > 210) & (saturation < 30)
    
    # Identify "Solid Matter" pixels (Anything that has color or is dark)
    # This captures the blue snakes, the warm skin, darkness, etc.
    solid_matter = ~is_bg_color
    
    # Create the Skeleton Mask
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[solid_matter] = 255
    
    # --- HOLE FILLING (Fixes Face/Eyes/Internal Holes) ---
    # We want to fill any black holes inside the white skeleton.
    
    # 1. Pad the image to ensure background is connected to outside
    # (Fixes "edge touching" bugs)
    pad = 10
    mask_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    
    # 2. Key Step: Flood Fill the Background (from 0,0)
    # This identifies the "True Outside".
    h_pad, w_pad = mask_padded.shape
    flood_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(mask_padded, flood_mask, (0,0), 255)
    
    # At this point, mask_padded has:
    # - Original Solid Matter (255)
    # - Background that was flooded (255)
    # - Internal Holes that were NOT flooded (0)  <-- Wait, floodFill fills with NewVal.
    
    # Let's do the "Inversion Trick" for Hole Filling properly:
    # A. Start with Skeleton.
    # B. FloodFill from (0,0) with GREY (128).
    # C. Anything that remains BLACK (0) was unreachable -> It is an Internal Hole.
    # D. Turn Internal Holes to WHITE (255).
    # E. Turn GREY back to BLACK (0).
    
    skeleton_padded = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    ff_mask = np.zeros((h_pad+2, w_pad+2), np.uint8)
    cv2.floodFill(skeleton_padded, ff_mask, (0,0), 128) # Fill background with 128
    
    # Now:
    # 255 = Original Unit
    # 128 = Background
    # 0 = Internal Holes (Face, Eyes, Weapon Center)
    
    final_mask_padded = skeleton_padded.copy()
    final_mask_padded[skeleton_padded == 0] = 255   # Fill holes
    final_mask_padded[skeleton_padded == 128] = 0   # Clear background
    
    # Crop back to original size
    final_mask = final_mask_padded[pad:-pad, pad:-pad]
    
    # --- EDGE TRIMMER (Fixes Sticker Border) ---
    # The mask ensures Solidity. Now we need to shave the white border.
    
    # Erode the WHOLE unit by 1px to clean dragon edges
    kernel = np.ones((2,2), np.uint8)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    
    # SPEAR SPECIFIC SHAVE
    # Create a wrapper for the spear tip (bottom left)
    spear_y0, spear_y1 = int(h*0.50), int(h*0.95)
    spear_x0, spear_x1 = int(w*0.0), int(w*0.50)
    
    h_idx, w_idx = np.indices((h, w))
    in_spear_box = (h_idx >= spear_y0) & (h_idx <= spear_y1) & (w_idx >= spear_x0) & (w_idx <= spear_x1)
    
    # Create a sub-mask for erosion
    # We want to erode the spear area MORE (to kill the sticker glow).
    # We iterate on the mask ONLY in that region.
    
    feature_mask = final_mask.copy()
    
    # Extract spear part
    spear_part = np.zeros_like(final_mask)
    spear_part[in_spear_box] = final_mask[in_spear_box]
    
    # Aggressively erode the spear part (2 more iterations) = Total 3px shaving
    spear_shaved = cv2.erode(spear_part, kernel, iterations=2)
    
    # Combine back:
    # Final = (Body - SpearArea) + ShavedSpear
    body_part = final_mask.copy()
    body_part[in_spear_box] = 0 # Remove old spear
    
    combined_mask = cv2.bitwise_or(body_part, spear_shaved)
    
    # Apply to Alpha
    rgba[:,:,3] = combined_mask
    rgba[combined_mask == 0, :3] = 0 # Cleaning ghost colors
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V90 COMPLETE: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v90_desticker(source, "public/assets/water_deity_unit_final.png")
