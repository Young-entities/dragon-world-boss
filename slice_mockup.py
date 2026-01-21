
import cv2
import numpy as np
import os

# Path to the mockup screenshot provided by the user
mockup_path = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\uploaded_image_1768930902356.png"
asset_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def slice_buttons():
    if not os.path.exists(mockup_path):
        print("Mockup file not found!")
        return

    img = cv2.imread(mockup_path)
    h, w = img.shape[:2]
    
    # We are looking for the bottom row.
    # The buttons are Blue, Green, Red.
    
    # 1. Define color ranges (HSV)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Blue Mask
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Green Mask
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Red Mask (Wrap around)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Function to find bounding box of the largest area
    def get_bbox(mask, name):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Sort by area
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 1000: # Filter noise
                x, y, w, h = cv2.boundingRect(c)
                # Expand slightly to capture the frame?
                # The mockup has a grey frame around the color.
                # Expanding by 15px looks safe based on the image.
                padding = 15
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = w + (padding * 2)
                h = h + (padding * 2)
                
                # Verify bounds
                crop = img[y:y+h, x:x+w]
                out_name = f"btn_{name}_exact.png"
                cv2.imwrite(os.path.join(asset_dir, out_name), crop)
                print(f"Extracted {name} to {out_name}")
                return True
        return False

    get_bbox(mask_blue, "blue")
    get_bbox(mask_green, "green")
    get_bbox(mask_red, "red")

slice_buttons()
