
import cv2
import numpy as np

def despill_green(input_path, output_path):
    print(f"Despilling green from: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found.")
        return

    if img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
    else:
        # If no alpha, treat as BGR
        b, g, r = cv2.split(img)
        a = None

    # Despill Logic:
    # Target pixels where Green > Red AND Green > Blue
    # Calculate spill amount
    
    # We want to clamp Green to be not much larger than the others.
    # Usually max(R, B).
    
    limit = np.maximum(r, b)
    
    # Mask where G > limit (Green dominant)
    mask = g > limit
    
    # Determine new Green value.
    # Standard despill: G = limit
    # This turns Pure Green (0, 255, 0) into (0, 0, 0) Black.
    # It turns Lime (128, 235, 0) into (128, 128, 0) Olive.
    
    # We can be slightly reduced strength if it kills too much color? 
    # But user hates green. Full despill is best.
    
    g_new = g.copy()
    g_new[mask] = limit[mask]
    
    # Update image
    img_new = cv2.merge([b, g_new, r, a])
    
    # Optional: If the pixel was pure green background (and transparent), changing G doesn't matter.
    # But if pixel was semi-transparent edge, this changes the visible color.
    
    cv2.imwrite(output_path, img_new)
    print(f"Saved despilled image to {output_path}")

path = "public/assets/celestial_valkyrie.png"
despill_green(path, path)
