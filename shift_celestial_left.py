
import cv2
import numpy as np

def shift_left(input_path, output_path, shift_amount=40):
    print(f"Shifting content left by {shift_amount}px: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    h, w = img.shape[:2]
    # Should be 900x600 from previous step
    
    # Extract Content first
    a = img[:, :, 3]
    coords = cv2.findNonZero(a)
    if coords is not None:
        x, y, cw, ch = cv2.boundingRect(coords)
        content = img[y:y+ch, x:x+cw]
        
        # Create empty canvas
        canvas = np.zeros((h, w, 4), dtype=np.uint8)
        
        # Calculate new position
        # Standard centered X was (900 - cw) // 2
        # We want to shift LEFT, so subtract from X
        
        # Current centered X approx (900 - cw)//2.
        # Let's verify if it was centered.
        # Previous script standardized it centered.
        
        new_x = ((w - cw) // 2) - shift_amount
        new_y = (h - ch) // 2 # Keep vertical center (it was 6px padding)
        
        # Ensure we don't go out of bounds
        if new_x < 0:
            print(f"Warning: Shift {shift_amount} clips content. Using {new_x}.")
            new_x = 0
            
        canvas[new_y:new_y+ch, new_x:new_x+cw] = content
        
        cv2.imwrite(output_path, canvas)
        print(f"Saved shifted image to {output_path}")

path = "public/assets/celestial_valkyrie.png"
shift_left(path, path, shift_amount=35) # 35px shift
