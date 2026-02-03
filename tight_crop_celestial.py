
import cv2
import numpy as np

def tight_crop(input_path, output_path):
    print(f"Tight cropping: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    # Find content
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            print(f"Content: {w}x{h} at {x},{y}")
            
            # Crop to content exactly
            # Add small padding (e.g. 5px) just to avoid raw edge touching
            pad = 5
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img.shape[1], x + w + pad)
            y2 = min(img.shape[0], y + h + pad)
            
            crop = img[y1:y2, x1:x2]
            
            cv2.imwrite(output_path, crop)
            print(f"Saved crop: {x2-x1}x{y2-y1}")

path = "public/assets/celestial_valkyrie.png"
tight_crop(path, path)
