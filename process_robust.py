import cv2
import numpy as np

def surgical_v70_robust_extract(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: 
        print(f"Could not load {input_path}")
        return
    
    # 1. Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # --- ROBUST EXTRACTION V70 ---
    # Simplified Logic: High Brightness + Low Saturation = Transparent
    
    b, g, r = cv2.split(img)
    
    # Calculate percieved brightness
    luma = 0.299*r + 0.587*g + 0.114*b
    
    # Calculate saturation
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    
    # 2. Define Background Mask
    # STRICTER Threshold: Must be very bright (>225) and very unsaturated (<15)
    # This catches "white" and "light grey" pixels.
    is_bg = (luma > 225) & (saturation < 15)
    
    # 3. Apply to Alpha
    # Start with full opaque
    alpha = np.ones_like(luma, dtype=np.uint8) * 255
    
    # Set background to 0 (Transparent)
    alpha[is_bg] = 0
    
    # 4. Face Protection (Keep this, it worked)
    h, w = img.shape[:2]
    h_idx, w_idx = np.indices((h, w))
    # Face is approx 20-35% down, 45-55% across
    face_y_min, face_y_max = int(h*0.20), int(h*0.35)
    face_x_min, face_x_max = int(w*0.42), int(w*0.58)
    
    face_mask = (h_idx >= face_y_min) & (h_idx <= face_y_max) & \
                (w_idx >= face_x_min) & (w_idx <= face_x_max)
    
    # Force face pixels to OPAQUE (255)
    alpha[face_mask] = 255

    # 5. Zonal Skin Protection (V71)
    # Only protect skin in the center column where the girl is.
    # Dragons on the sides have orange rust that we want to KILL.
    # Column: 30% to 70% width
    center_x_min, center_x_max = int(w*0.30), int(w*0.70)
    
    is_skin_color = (r > g) & (g > b) & (r > 150)
    
    # Create a spatial mask for the "Body Column"
    body_mask = np.zeros_like(luma, dtype=bool)
    body_mask[:, center_x_min:center_x_max] = True
    
    # Only protect skin if it's in the body column
    final_skin_mask = is_skin_color & body_mask
    
    alpha[final_skin_mask] = 255
    
    # 6. Edge Cleaning (Kill White Outline)
    # Erode the alpha mask by 1 pixel to eat the white fringe
    kernel = np.ones((2,2), np.uint8)
    alpha_cleaned = cv2.erode(alpha, kernel, iterations=1)
    
    # 7. Save
    rgba[:,:,3] = alpha_cleaned
    
    # Cleanup ghost rgb
    # where alpha is 0, set rgb to 0 to avoid "glow" interpolation
    rgba[alpha_cleaned == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Robust Extraction Complete: {output_path}")

source = r"C:\\Users\\kevin\\New folder (2)\\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v70_robust_extract(source, "public/assets/water_deity_unit_final.png")
