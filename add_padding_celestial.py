
import cv2
import numpy as np

def add_padding(input_path, output_path, scale=0.85):
    print(f"Adding padding to: {input_path} (Scale: {scale})")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found.")
        return

    # Ensure Alpha
    if img.shape[2] < 4:
        print("Error: No alpha channel.")
        return

    h, w = img.shape[:2]
    
    # Calculate new dimensions
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Resize content
    # Use INTER_AREA for shrinking to preserve quality
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Create empty canvas of original size
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    
    # Calculate Center Offsets
    x_off = (w - new_w) // 2
    y_off = (h - new_h) // 2
    
    # Paste
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized
    
    cv2.imwrite(output_path, canvas)
    print(f"Saved padded image to {output_path}")

path = "public/assets/celestial_valkyrie.png"
add_padding(path, path, scale=0.80) # Using 80% to be safe and ensure she fits comfortably
