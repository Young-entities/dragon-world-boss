
import cv2
import numpy as np
import os

mockup_path = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\uploaded_image_1768930902356.png"
asset_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def slice_buttons_v2():
    if not os.path.exists(mockup_path):
        print("Mockup file not found!")
        return

    img = cv2.imread(mockup_path)
    h, w = img.shape[:2]
    
    # 0. ROI: Only look at bottom 30% of the screen
    roi_y = int(h * 0.70)
    roi = img[roi_y:h, 0:w]
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Blue Mask
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Green Mask
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Red Mask 
    # Tighter Red to avoid orange fire
    lower_red1 = np.array([0, 150, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 100])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Debug: Save mask
    cv2.imwrite(os.path.join(asset_dir, "debug_red_mask.png"), mask_red)

    def get_bbox(mask, name):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Pick largest contour that is "Button Shaped" (Aspect ratio > 2.0?)
            # Buttons are wide.
            valid_contours = []
            for c in contours:
                x, y, cw, ch = cv2.boundingRect(c)
                if cw > 50 and ch > 20: # Min size
                    valid_contours.append((c, cw*ch))
            
            if valid_contours:
                c = max(valid_contours, key=lambda item: item[1])[0]
                x, y, cw, ch = cv2.boundingRect(c)
                
                padding = 15
                
                # Careful not to go out of bounds of ROI
                y_global = roi_y + y
                x_global = x
                
                # Expand
                y_start = max(0, y_global - padding)
                y_end = min(h, y_global + ch + padding)
                x_start = max(0, x_global - padding)
                x_end = min(w, x_global + cw + padding)
                
                crop = img[y_start:y_end, x_start:x_end]
                out_name = f"btn_{name}_exact.png"
                out_path = os.path.join(asset_dir, out_name)
                cv2.imwrite(out_path, crop)
                print(f"Extracted {name} to {out_path} (Size: {crop.shape})")
                return True
        print(f"Failed to find {name}")
        return False

    get_bbox(mask_blue, "blue")
    get_bbox(mask_green, "green")
    get_bbox(mask_red, "red")

slice_buttons_v2()
