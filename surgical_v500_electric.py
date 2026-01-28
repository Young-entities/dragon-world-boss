import cv2
import numpy as np

def surgical_v500_electric(input_path, output_path):
    print(f"Processing: {input_path}")
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Input image not found.")
        return

    b, g, r = cv2.split(img)
    
    # Logic from v310:
    # Green BG: G > R+20 AND G > B+20.
    # Electric Unit is Yellow (R+G) and Blue (B).
    # Yellow (255, 255, 0) -> G ~ R. Condition G > R+20 Fails. Safe.
    # Blue (0, 0, 255) -> G < B+20. Safe.
    # Cyan (0, 255, 255) -> G ~ B. Safe.
    # So this logic works perfectly for Electric units too.
    
    is_green_bg = (g.astype(int) > r.astype(int) + 30) & \
                  (g.astype(int) > b.astype(int) + 30) & \
                  (g > 60)
                  
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # Despill (G = min(G, max(R, B)))
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    # Reducing green channel where it exceeds the max of others (green cast)
    new_g = np.minimum(new_g, max_rb)
    
    # Polish: Gaussian Blur on alpha to smooth jagged pixel edges
    # Standard erode might be too harsh for fine lightning details.
    # I'll use a very soft feathering.
    
    # Refine mask
    alpha_float = alpha.astype(float) / 255.0
    alpha_blurred = cv2.GaussianBlur(alpha_float, (3, 3), 0)
    
    # Re-binarize/Clamp lightly? No, let's keep soft edges for glow.
    # Actually, sprite edges usually need to be sharp-ish.
    # Let's just erode 1 pixel if needed.
    # Previous v310 eroded 2x2. I'll stick to that as it cleaned well.
    kernel = np.ones((2,2), np.uint8)
    alpha_cleaned = cv2.erode(alpha, kernel, iterations=1)
    
    # Save
    final_img = cv2.merge([b, new_g, r, alpha_cleaned])
    
    # Ensure fully transparent pixels are black 
    # (Optional, but good for some renderers)
    # final_img[alpha_cleaned == 0] = 0 
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V500 Electric Extraction Complete: {output_path}")

# Run
input_file = "c:/Users/kevin/New folder (2)/electric_god_unit.png"
output_file = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/electric_god_unit_clean.png"

surgical_v500_electric(input_file, output_file)
