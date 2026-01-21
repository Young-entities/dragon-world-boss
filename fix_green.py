
import cv2
import numpy as np
import os

path = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets\btn_green.png"

def fix_green():
    if not os.path.exists(path):
        print("File not found")
        return

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    
    # Check if it has alpha
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # It seems the previous script might have failed or the "White Box" is actually white pixels.
    # Let's check the corners.
    corner = img[0,0]
    print(f"Corner: {corner}")
    
    # If corner is White (255, 255, 255), remove white.
    # If corner is Black (0, 0, 0), remove black.
    
    # Create mask for White-ish pixels (> 200)
    white_mask = np.all(img[:, :, :3] > 200, axis=2)
    # And mask for Black-ish pixels (< 50)
    black_mask = np.all(img[:, :, :3] < 50, axis=2)
    
    # We need to decide which to remove.
    # Count corner pixels
    corners = [img[0,0], img[0,-1], img[-1,0], img[-1,-1]]
    is_white_bg = all(np.mean(c[:3]) > 200 for c in corners)
    
    if is_white_bg:
        print("Detected White Background. Removing...")
        img[white_mask] = [0, 0, 0, 0]
    else:
        print("Detected Dark/Black Background. Removing...")
        # Remove Black Background
        # Also remove "near black" to kill artifacts
        # We need to be careful not to kill the dark metal frame.
        # Floodfill from 0,0 is safest.
        h, w = img.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        # Floodfill from 0,0 with tolerance
        cv2.floodFill(img, mask, (0,0), (0,0,0,0), (20,20,20), (20,20,20), cv2.FLOODFILL_FIXED_RANGE)
        
        # Do other corners too
        cv2.floodFill(img, mask, (w-1,0), (0,0,0,0), (20,20,20), (20,20,20), cv2.FLOODFILL_FIXED_RANGE)
        cv2.floodFill(img, mask, (0,h-1), (0,0,0,0), (20,20,20), (20,20,20), cv2.FLOODFILL_FIXED_RANGE)
        cv2.floodFill(img, mask, (w-1,h-1), (0,0,0,0), (20,20,20), (20,20,20), cv2.FLOODFILL_FIXED_RANGE)

    cv2.imwrite(path, img)
    print("Fixed btn_green.png")

fix_green()
