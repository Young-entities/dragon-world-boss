import cv2
import numpy as np

def simple_white_removal(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. Targeted White Range
    # Most white backgrounds are very close to 255.
    lower_white = np.array([245, 245, 245])
    upper_white = np.array([255, 255, 255])
    white_mask = cv2.inRange(img, lower_white, upper_white)
    
    # 2. Character Protection (Face/Skin)
    # The face is approx (654, 252) on the high-res 1312x800 image.
    # We protect this area so the white-removal doesn't create holes in her skin.
    shield = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(shield, (654, 250), 100, 255, -1) # Face area
    cv2.rectangle(shield, (600, 350), (700, 700), 255, -1) # Body skin line
    
    # 3. Apply Transparency
    # Alpha = 0 for white pixels, unless they are shielded.
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    alpha[(white_mask == 255) & (shield == 0)] = 0
    alpha[shield == 255] = 255
    
    # 4. FloodFill from corners to clean up outer edges
    # This ensures the rectangular background box is 100% gone.
    flood_mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(alpha, flood_mask, (0,0), 0)
    cv2.floodFill(alpha, flood_mask, (w-1,0), 0)
    
    rgba[:,:,3] = alpha
    
    # Save (Minimal 5px margin only to avoid cut-off)
    rgba = rgba[5:h-5, 5:w-5]
    
    cv2.imwrite(output_path, rgba)
    print(f"White transparency applied: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_7kxmfb7kxmfb7kxm.png"
simple_white_removal(source, "public/assets/water_deity_unit_final.png")
