import cv2
import numpy as np

def create_dark_icon(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Image not found")
        return

    # Split
    b, g, r, a = cv2.split(img)
    
    # Convert BGR to HSV
    bgr = cv2.merge([b, g, r])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Hue Shift
    # Fire is Red (0) / Orange (15) / Yellow (30).
    # Purple is ~135-150 in OpenCV (270-300 deg).
    # Shift H by +135
    
    h_new = (h.astype(np.int16) + 135) % 180
    h_new = h_new.astype(np.uint8)
    
    # Darken slightly?
    # v = (v * 0.9).astype(np.uint8)
    
    hsv_new = cv2.merge([h_new, s, v])
    bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    b_new, g_new, r_new = cv2.split(bgr_new)
    
    rgba = cv2.merge([b_new, g_new, r_new, a])
    
    cv2.imwrite(output_path, rgba)
    print(f"Created Dark Icon: {output_path}")

create_dark_icon("public/assets/element_fire_v4.png", "public/assets/element_dark.png")
