import cv2
import numpy as np

def clean_portrait_v2(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    
    # 1. REMOVE DIAMOND (Bottom Right)
    # The diamond is in the absolute bottom-right corner.
    # We patch it with surrounding theme colors.
    patch_size = 90
    corner_y = h - patch_size
    corner_x = w - patch_size
    
    # Average color of the area just above/left of the corner
    sample = img[h-130:h-90, w-130:w-90]
    avg_color = np.median(sample.reshape(-1, 3), axis=0)
    
    img[corner_y:, corner_x:] = avg_color
    
    cv2.imwrite(output_path, img)
    print(f"Cleaned Portrait V2 saved: {output_path}")

clean_portrait_v2("public/assets/overlord_portrait_v2.png", "public/assets/overlord_portrait_v2_clean.png")
