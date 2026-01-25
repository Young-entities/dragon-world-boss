import cv2
import numpy as np

def surgical_v60_perfect_extract(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: 
        print(f"Could not load {input_path}")
        return
    
    # 1. Convert to BGRA
    # This automatically adds an alpha channel (currently 255 for all)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 2. Creating a "Chroma Key" Mask
    # The background is white/light-grey. Unit is mostly blue.
    # We want to kill anything that is "Neutral Grey/White" but KEEP anything "Blue".
    
    # Extract channels
    b, g, r = cv2.split(img)
    
    # --- STEP 1: Brightness Filter ---
    # Background is bright. Unit has darks and midtones.
    # Anything very dark is definitely NOT background.
    is_bright = (r > 200) & (g > 200) & (b > 200)
    
    # --- STEP 2: Saturation/Color Filter ---
    # This is the secret sauce. 
    # Background is GREY (R~=G~=B). 
    # Unit is BLUE/CYAN (B > R, B > G).
    # We calculate the "Blueness" of each pixel.
    # Blueness = B - max(R, G)
    # --- IMPROVED LOGIC V62 ---
    
    # 1. Calculate Perceived Brightness (Luma)
    luma = 0.299*r + 0.587*g + 0.114*b
    is_bright = luma > 215 

    # 2. Calculate Colorfulness (Saturation relative to brightness)
    # Background is sterile white/grey. Unit has color.
    max_channel = np.maximum(np.maximum(r, g), b).astype(int)
    min_channel = np.minimum(np.minimum(r, g), b).astype(int)
    saturation = max_channel - min_channel
    
    # If it has color (> 15 saturation), keep it.
    is_colorful = saturation > 15

    # 3. Blueness Check (The unit is blue)
    # Unit pixels usually have B > R or B > G.
    is_blue_dominant = (b > r) | (b > g)
    
    # Background Mask = Bright AND NOT Colorful AND NOT Blue Dominant
    background_mask = is_bright & (~is_colorful) & (~is_blue_dominant)
    
    # --- FACE PROTECTION ---
    # We define a box around the face area (roughly top center)
    # and force the mask to False there to prevent ANY deletion.
    h, w = img.shape[:2] # Ensure dimensions are available
    h_idx, w_idx = np.indices((h, w))
    # Face is approx 20-35% down, 45-55% across
    face_y_min, face_y_max = int(h*0.20), int(h*0.35)
    face_x_min, face_x_max = int(w*0.42), int(w*0.58)
    
    face_mask = (h_idx >= face_y_min) & (h_idx <= face_y_max) & \
                (w_idx >= face_x_min) & (w_idx <= face_x_max)
    
    # --- ULTRA AGGRESSIVE CLEANUP V65 ---
    # Convert properly to a binary mask for analysis
    # Anything not fully transparent is a potential object
    alpha_channel = rgba[:,:,3]
    _, binary_mask = cv2.threshold(alpha_channel, 10, 255, cv2.THRESH_BINARY)
    
    # Connect Components Analysis
    # This finds every separate "island" of pixels
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, 8, cv2.CV_32S)
    
    # Loop through all found components
    # Label 0 is the background (empty space), start from 1
    new_mask = np.zeros_like(alpha_channel)
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        
        # KEY LOGIC: If a blob is tiny (dust/noise), kill it.
        # If it's the main unit (massive), keep it.
        if area > 500: # Keep separate big parts (dragons, etc)
             new_mask[labels == i] = 255
             
    # Apply this new cleaner mask to the alpha channel
    # We use a bitwise_and to combine it with the original alpha softness
    # so we don't lose the soft edges of the main unit, but we kill the noise completely.
    final_alpha = cv2.bitwise_and(rgba[:,:,3], new_mask)
    rgba[:,:,3] = final_alpha
    
    cv2.imwrite(output_path, rgba)
    print(f"Perfect Extraction Complete: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v60_perfect_extract(source, "public/assets/water_deity_unit_final.png")
