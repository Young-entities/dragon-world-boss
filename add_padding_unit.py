import cv2
import numpy as np

def add_padding(input_path, output_path, padding_percent=0.15):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Image not found")
        return

    h, w = img.shape[:2]
    
    pad_h = int(h * padding_percent)
    pad_w = int(w * padding_percent)
    
    # Create new larger canvas (transparent)
    new_h = h + 2 * pad_h
    new_w = w + 2 * pad_w
    
    # Initialize with alpha=0
    canvas = np.zeros((new_h, new_w, 4), dtype=np.uint8)
    
    # Center the original image
    canvas[pad_h:pad_h+h, pad_w:pad_w+w] = img
    
    cv2.imwrite(output_path, canvas)
    print(f"Added Padding ({padding_percent*100}%): {output_path}")

add_padding("public/assets/dark_deity_unit.png", "public/assets/dark_deity_unit.png", 0.15)
