import cv2
import numpy as np

def force_purple_circle(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Image not found")
        return

    # Split channels
    b, g, r, a = cv2.split(img)
    bgr = cv2.merge([b, g, r])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Define ROI: Bottom 30% (The Magic Circle on ground)
    height, width = img.shape[:2]
    roi_top = int(height * 0.7)
    
    # Create spatial mask (Bottom area)
    spatial_mask = np.zeros((height, width), dtype=np.uint8)
    spatial_mask[roi_top:, :] = 255
    
    # Define Color Mask for Brown/Orange/Reddish-Purple
    # Brown/Orange: H=5 to 25.
    # Reddish Purple: H=160 to 180 (OpenCV wraps Red).
    # Gold Armor is usually H=30+ in bright areas?
    # Brown is Dark Orange.
    
    # Mask 1: Orange/Brown (Hue 5-25)
    mask1 = cv2.inRange(hsv, np.array([5, 30, 30]), np.array([25, 255, 255]))
    
    # Mask 2: Reddish (Hue 0-5 and 170-180)
    mask2 = cv2.inRange(hsv, np.array([0, 30, 30]), np.array([5, 255, 255]))
    mask3 = cv2.inRange(hsv, np.array([170, 30, 30]), np.array([180, 255, 255]))
    
    color_mask = mask1 | mask2 | mask3
    
    # Combine Spatial and Color Mask
    target_mask = (spatial_mask > 0) & (color_mask > 0)
    
    # Apply Shift to Purple (Hue 140)
    h[target_mask] = 140
    # Boost Saturation to make it glow
    s[target_mask] = np.clip(s[target_mask] + 40, 0, 255)
    
    # Rebuild
    hsv_new = cv2.merge([h, s, v])
    bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    
    b_new, g_new, r_new = cv2.split(bgr_new)
    
    # Update localized pixels
    b[target_mask] = b_new[target_mask]
    g[target_mask] = g_new[target_mask]
    r[target_mask] = r_new[target_mask]
    
    rgba = cv2.merge([b, g, r, a])
    
    cv2.imwrite(output_path, rgba)
    print(f"Force Purple Circle Complete: {output_path}")

force_purple_circle("public/assets/dark_deity_unit.png", "public/assets/dark_deity_unit.png")
