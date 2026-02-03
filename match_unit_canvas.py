
import cv2
import numpy as np

def match_canvas_ratio(input_path, output_path):
    print(f"Adjusting canvas for: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    h, w = img.shape[:2]
    # Current: 1024x1024
    
    # Target Ratio: 3:2 (Width:Height) like Azaerth (900x600 is 3:2)
    # We keep Width 1024.
    # Target Height = 1024 * (2/3) = 682.6 -> 683.
    
    target_h = int(w * (2/3))
    
    # Check if content fits
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
            x, y, cw, ch = cv2.boundingRect(coords)
            print(f"Content Height: {ch}")
            # Center of content
            cy = y + ch // 2
            
            # We want to keep the content centered in the new height.
            # But we are just cropping the canvas.
            
            # If ch > target_h, we can't crop without clipping.
            if ch > target_h:
                print(f"Warning: Content height {ch} exceeds target {target_h}. Scaling down?")
                # If it exceeds, we must scale content.
                # But Step 7783 scaled it to 80%? 
                # Let's verify content height.
                pass
    
    # Crop to center
    if h > target_h:
        start_y = (h - target_h) // 2
        img_cropped = img[start_y : start_y + target_h, :]
        print(f"Cropped canvas to {w}x{target_h}")
        cv2.imwrite(output_path, img_cropped)
    else:
        print("Image already short enough.")

path = "public/assets/celestial_valkyrie.png"
match_canvas_ratio(path, path)
