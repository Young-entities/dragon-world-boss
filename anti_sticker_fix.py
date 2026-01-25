import cv2
import numpy as np

def anti_sticker_fix(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # 1. AGGRESSIVE FRINGE REMOVAL
    # We will erode the alpha channel to cut past the white "halo" pixels
    kernel = np.ones((3,3), np.uint8)
    # 2 iterations to really get past the fuzzy white ghosting
    a_eroded = cv2.erode(a, kernel, iterations=2)
    
    # 2. EDGE SOFTENING (Feathering)
    # This removes the "sharp scissor cut" look and makes it blend with the background
    a_feathered = cv2.GaussianBlur(a_eroded, (5,5), 0)
    
    # 3. COLOR DEFARING (Optional but helpful)
    # We can slightly darken the edges of the colorful channels where they meet the transparency
    # but the aggressive erosion is usually enough.
    
    result = cv2.merge([b, g, r, a_feathered])
    cv2.imwrite(output_path, result)
    print(f"Anti-sticker professional blending completed: {output_path}")

# Run on the source white-bg image to ensure we have the best starting point
anti_sticker_fix("public/assets/overlord_white_bg.png", "public/assets/overlord_pro_blended.png")
