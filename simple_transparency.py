import cv2
import numpy as np

def surgical_v21_pure_clean(input_path, output_path):
    # Load EXACT generated image
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Intelligent Edge Fill
    mask = np.zeros((h + 2, w + 2), np.uint8)
    fill_color = (255, 0, 255) # Magenta
    
    # Fill from corners with 0 tolerance to avoid any "eating" of the art
    # The source is pure white, so 0 is safest
    cv2.floodFill(img, mask, (0,0), fill_color, (0, 0, 0), (0, 0, 0))
    cv2.floodFill(img, mask, (w-1, 0), fill_color, (0, 0, 0), (0, 0, 0))
    cv2.floodFill(img, mask, (0, h-1), fill_color, (0, 0, 0), (0, 0, 0))
    cv2.floodFill(img, mask, (w-1, h-1), fill_color, (0, 0, 0), (0, 0, 0))
    
    # Transparency rule
    bg_mask = (img[:,:,0] == 255) & (img[:,:,1] == 0) & (img[:,:,2] == 255)
    rgba[bg_mask, 3] = 0
    
    # NO RESIZING, NO NOSE, NO FADING.
    cv2.imwrite(output_path, rgba)
    print(f"Pure original transparency complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
surgical_v21_pure_clean(source, "public/assets/water_deity_unit_final.png")
