import cv2
import numpy as np

def surgical_v40_conservative_halo_fix(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. IDENTIFY BACKGROUND (Connected White)
    # We flood-fill from the corners with a healthy tolerance (45)
    # This specifically targets the "white halo" connected to the outside.
    temp_img = img.copy()
    mask = np.zeros((h+2, w+2), np.uint8)
    fill_color = (255, 0, 255) # Magenta
    
    # Corners and edges to swallow the outer white rectangle and outlines
    edge_pts = [(0,0), (w-1, 0), (0, h-1), (w-1, h-1), (w//2, 0), (0, h//2), (w-1, h//2)]
    for pt in edge_pts:
        cv2.floodFill(temp_img, mask, pt, fill_color, (45, 45, 45), (45, 45, 45))
    
    # 2. IDENTIFY INTERNAL WHITE ISLANDS (Gaps between dragons)
    # We use a strict range so we don't eat her armor highlights
    lower_white = np.array([240, 240, 240])
    upper_white = np.array([255, 255, 255])
    internal_white = cv2.inRange(img, lower_white, upper_white)
    
    # 3. PROTECTION (The Solid Core)
    # We protect the entire unit's core frame to stop "holes" from appearing
    shield = np.zeros((h, w), dtype=np.uint8)
    # Scaled coordinates for 1312x800
    cv2.circle(shield, (654, 252), 110, 255, -1) # Face area
    cv2.rectangle(shield, (520, 250), (780, 800), 255, -1) # Body center
    
    # 4. FINAL ALPHA ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    
    # Rule 1: Outer background (Magenta from FloodFill) = Transparent
    is_outer_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    alpha[is_outer_bg] = 0
    
    # Rule 2: Internal White (If not shielded) = Transparent
    alpha[(internal_white == 255) & (shield == 0)] = 0
    
    # Rule 3: Absolute Solid Face/Core
    alpha[shield == 255] = 255
    
    # 5. HALO SUPPRESSION (Edge Tightening)
    # Only shrink the transparency edges by 1 pixel to clean up the weapon/head outline
    # but don't eat into her blue armor.
    kernel = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel) # Removes tiny stray pixels
    
    rgba[:,:,3] = alpha
    
    # 6. SAVE (No aggressive crop)
    rgba = rgba[10:h-45, 10:w-10]
    
    cv2.imwrite(output_path, rgba)
    print(f"Conservative Halo Fix complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
surgical_v40_conservative_halo_fix(source, "public/assets/water_deity_unit_final.png")
