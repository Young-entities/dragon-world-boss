import cv2
import numpy as np

def surgical_v45_nuke_diamond(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    h, w = img.shape[:2]

    # If it's not already 4 channels, convert
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Target the bottom right diamond (approx 100px from right, 100px from bottom)
    # We'll just transparentize that specific small region if it contains 'grey/white'
    roi_x, roi_y = w - 100, h - 80
    roi_w, roi_h = 80, 60
    
    # Create a mask for that region
    # Any pixel in this region that is very bright/neutral (the diamond)
    roi = img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    
    # Define diamond color (light grey/white)
    lower_white = np.array([120, 120, 120, 0])
    upper_white = np.array([255, 255, 255, 255])
    
    diamond_mask = cv2.inRange(roi, lower_white, upper_white)
    
    # Set those pixels to zero alpha
    roi[diamond_mask == 255, 3] = 0
    img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = roi
    
    cv2.imwrite(output_path, img)
    print(f"Diamond Nuked: {output_path}")

source = "public/assets/water_deity_unit_final.png" # Working on the current transparent version
surgical_v45_nuke_diamond(source, "public/assets/water_deity_unit_final.png")
