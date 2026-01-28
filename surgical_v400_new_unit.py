import cv2
import numpy as np
import os

def surgical_v400_new_unit(input_path, output_path):
    print(f"Processing New Unit: {input_path}")
    
    # Read Image (Handle Absolute Path)
    # The path contains spaces or special chars? Python strings handle it.
    # But Windows paths use backslashes.
    input_path = input_path.replace("\\", "/")
    
    img = cv2.imread(input_path)
    if img is None: 
        print(f"Error: Could not read {input_path}")
        return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # GREEN EXTRACTION
    # Check if Green Dominant (just to be safe)
    avg_color = np.mean(img, axis=(0,1)) # BGR
    print(f"Average Color: {avg_color}")
    
    # Standard Green Screen Logic
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # DESPILL (Blue/Cyan Unit)
    # Target is Water/Ice (Blue/Cyan).
    # Cyan = G+B.
    # Green BG = G.
    # If G is clamped to max(R, B), Cyan loses its Green component -> becomes Blue.
    # This might darken the Cyan crystals.
    # Ice Blue `(0, 255, 255)`. Despill -> `min(255, 255) = 255`. Safe.
    # Pure Green `(0, 255, 0)`. Despill -> `min(255, 0) = 0`. Safe.
    # So Standard Despill is safe for Cyan.
    
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb)
    
    # TEXT/FRAME CROP?
    # Sometimes generation adds a text box at bottom.
    # Detect solid block at bottom?
    # Let's assume clean for now.
    
    # POLISH
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, new_g, r, alpha])
    final_img[alpha == 0] = 0
    
    # Ensure directory exists?
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V400 New Unit Complete: {output_path}")

# Run
input_file = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_fortress_unit_1769482505730.png"
output_file = "public/assets/crystal_fortress_unit.png"

surgical_v400_new_unit(input_file, output_file)
