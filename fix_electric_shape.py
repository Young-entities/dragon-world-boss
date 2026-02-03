
import cv2
import numpy as np

def fix_electric_shape(input_path, output_path):
    print(f"Fixing shape for: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Image not found")
        return

    # Check content aspect ratio
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            print(f"Content: {w}x{h}")
            
            content = img[y:y+h, x:x+w]
            
            # We want it to be Square (Circular look)
            # If w != h, stretch to match
            target_size = max(w, h)
            
            # Stretch content
            # This "squashes" or "stretches" the pixels to fit square shape.
            # User wants it like Units Tab (which likely stretches it).
            new_content = cv2.resize(content, (target_size, target_size), interpolation=cv2.INTER_AREA)
            
            # Create new square canvas
            # Use original canvas size or target size?
            # Original was 56x56. Let's keep 56x56.
            
            H, W = img.shape[:2]
            canvas = np.zeros((H, W, 4), dtype=np.uint8)
            
            # Center new content
            # Resize new_content to fit inside H,W if needed?
            # If target_size > H, resize down.
            if target_size > H:
                 new_content = cv2.resize(new_content, (H, H), interpolation=cv2.INTER_AREA)
                 target_size = H
            
            x_off = (W - target_size) // 2
            y_off = (H - target_size) // 2
            
            canvas[y_off:y_off+target_size, x_off:x_off+target_size] = new_content
            
            cv2.imwrite(output_path, canvas)
            print(f"Saved fixed shape to {output_path}")

path = "public/assets/element_electric.png"
fix_electric_shape(path, path)
