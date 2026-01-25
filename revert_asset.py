import cv2
import numpy as np

def absolute_revert_pure(input_path, output_path):
    # Load EXACT generated image
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Simple Edge-Fill only. No fading. No internal island removal.
    # This leaves the original AI art 100% intact.
    mask = np.zeros((h + 2, w + 2), np.uint8)
    fill_color = (255, 0, 255) # Magenta
    
    # Fill from edges with 0 tolerance
    cv2.floodFill(img, mask, (0,0), fill_color, (0, 0, 0), (0, 0, 0))
    cv2.floodFill(img, mask, (w-1, 0), fill_color, (0, 0, 0), (0, 0, 0))
    
    # Alpha rule: Only the magenta exterior is transparent
    bg_mask = (img[:,:,0] == 255) & (img[:,:,1] == 0) & (img[:,:,2] == 255)
    rgba[bg_mask, 3] = 0
    
    # Save the original sprite exactly as it was
    cv2.imwrite(output_path, rgba)
    print(f"Reverted to Pure Original: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
absolute_revert_pure(source, "public/assets/water_deity_unit_final.png")
