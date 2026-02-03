
import cv2
import numpy as np

def standardize_canvas(input_path, output_path):
    print(f"Standardizing to 900x600: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    # Dimensions of Azaerth Box
    CANVAS_W = 900
    CANVAS_H = 600
    PADDING = 6 # Top/Bottom padding like Azaerth
    
    # Target Content Height
    TARGET_CONTENT_H = CANVAS_H - (PADDING * 2) # 588
    
    # Current Size
    h, w = img.shape[:2]
    
    # Assuming input is tightly clipped (from previous step 7821 crop: 798x679)
    # We resize preserving aspect ratio to match TARGET_CONTENT_H
    
    scale = TARGET_CONTENT_H / h
    new_w = int(w * scale)
    new_h = int(h * scale) # Should be 588
    
    print(f"Resizing content to {new_w}x{new_h}")
    
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Create Canvas
    canvas = np.zeros((CANVAS_H, CANVAS_W, 4), dtype=np.uint8)
    
    # Paste Centered
    x_off = (CANVAS_W - new_w) // 2
    y_off = (CANVAS_H - new_h) // 2
    
    # Check bounds
    y1 = y_off
    y2 = y_off + new_h
    x1 = x_off
    x2 = x_off + new_w
    
    canvas[y1:y2, x1:x2] = resized
    
    cv2.imwrite(output_path, canvas)
    print(f"Saved standardized image to {output_path}")

path = "public/assets/celestial_valkyrie.png"
standardize_canvas(path, path)
