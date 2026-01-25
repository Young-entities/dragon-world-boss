import cv2
import numpy as np

def clean_new_face_icon(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    
    # 1. REMOVE DIAMOND (Bottom Right)
    # Wiping the extreme bottom-right corner 80x80
    corner_patch_y = h - 80
    corner_patch_x = w - 80
    
    # Get average color from just above the corner for a natural patch
    surroundings = img[h-120:h-80, w-120:w-80]
    avg_color = np.median(surroundings.reshape(-1, 3), axis=0)
    
    # Wipe it
    img[corner_patch_y:, corner_patch_x:] = avg_color
    
    cv2.imwrite(output_path, img)
    print(f"New face icon cleaned and saved: {output_path}")

clean_new_face_icon("public/assets/overlord_new_face.png", "public/assets/overlord_new_face_clean.png")
