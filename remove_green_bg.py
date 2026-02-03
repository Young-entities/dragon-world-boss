
import cv2
import numpy as np

def remove_green_background(input_path, output_path):
    # Load image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load {input_path}")
        return

    # Convert to standard RGBA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Convert to HSV for color segmentation
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    
    # Define Green range (Emerald Green)
    # Green is approx 60 degrees. 40-80 in OpenCV (scale 0-180)
    lower_green = np.array([35, 30, 30])
    upper_green = np.array([90, 255, 255])
    
    # Create mask for green
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Refine mask:
    # We want to keep NON-green things.
    # Invert mask: 0 = green (transparent), 255 = non-green (opaque)
    alpha_mask = cv2.bitwise_not(green_mask)
    
    # Clean up the mask using morphology to remove noise
    kernel = np.ones((3,3), np.uint8)
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_CLOSE, kernel)
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_OPEN, kernel)
    
    # Soften edges
    alpha_mask = cv2.GaussianBlur(alpha_mask, (3,3), 0)
    
    # Apply mask to alpha channel
    img[:, :, 3] = alpha_mask
    
    # Save
    cv2.imwrite(output_path, img)
    print(f"Saved transparent image to {output_path}")

input_file = "public/assets/eternal_lion_emperor.png"
output_file = "public/assets/eternal_lion_emperor.png"

remove_green_background(input_file, output_file)
