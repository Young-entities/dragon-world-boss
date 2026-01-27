import cv2
import numpy as np
import glob
import os

def surgical_v310_fire_green(output_path):
    # 1. FIND SOURCE (Newest PNG)
    # The user says "added same image in root".
    files = glob.glob("../*.png")
    if not files: 
        print("No source files found!")
        return
    
    # Sort by time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Detected Source: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None: return

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # 2. GREEN EXTRACTION (The Easy Way)
    # Standard: G dominant over R and B.
    # But wait, Fire is Yellow (R+G).
    # Green Screen is Pure Green (G >> R).
    # Fire/Yellow: R ~ G.
    # Green BG: G >> R.
    # Logic: G > R + 20?
    # Yellow: 200 > 255 + 20 (False). Safe.
    # Green: 255 > 0 + 20 (True). Extracted.
    
    is_green_bg = (g.astype(int) > r.astype(int) + 20) & \
                  (g.astype(int) > b.astype(int) + 20) & \
                  (g > 50)
    
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_green_bg] = 0
    
    # 3. DESPILL
    # Removing green reflection.
    # Fire Unit means lots of Red/Yellow.
    # Formula: G = min(G, max(R, B))
    # Yellow (255, 255, 0): max(R,B)=255. min(255, 255)=255. Safe.
    # Cyan Ice (0, 255, 255): max(R,B)=255. min(255, 255)=255. Safe.
    # Green BG (0, 255, 0): max(R,B)=0. min(255, 0)=0. Despilled to Black.
    
    new_g = g.copy()
    max_rb = np.maximum(r, b)
    new_g = np.minimum(new_g, max_rb)
    
    # 4. POLISH
    # 1px Shave to kill borders
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # Clean Corners (Safety)
    corner = 20
    alpha[0:corner, 0:corner] = 0
    alpha[0:corner, -corner:] = 0
    alpha[-corner:, 0:corner] = 0
    alpha[-corner:, -corner:] = 0

    # Save
    final_img = cv2.merge([b, new_g, r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V310 Fire Green Complete: {output_path}")

surgical_v310_fire_green("public/assets/overlord_absolute_final.png")
