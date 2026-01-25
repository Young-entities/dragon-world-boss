import cv2
import numpy as np

def clean_face_card(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    
    # 1. REMOVE DIAMOND (Bottom Right)
    # Wiping the extreme bottom-right corner 100x100
    # and filling it with the average color of the surrounding area
    corner_patch_y = h - 100
    corner_patch_x = w - 100
    
    # Get average color of the area just above the corner
    surroundings = img[h-150:h-100, w-150:w-100]
    avg_color = np.median(surroundings.reshape(-1, 3), axis=0)
    
    # Wipe the corner
    img[corner_patch_y:, corner_patch_x:] = avg_color
    
    cv2.imwrite(output_path, img)
    print(f"Face card cleaned and saved: {output_path}")

clean_face_card("public/assets/overlord_face_card.png", "public/assets/overlord_face_card_clean.png")
