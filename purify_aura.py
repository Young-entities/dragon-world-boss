import cv2
import numpy as np

def purify_aura(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED) # Load RGBA
    if img is None:
        print("Image not found")
        return

    if img.shape[2] < 4:
        print("Image has no alpha channel")
        return

    # Split channels
    b, g, r, a = cv2.split(img)
    
    # Convert BGR to HSV for color detection
    bgr = cv2.merge([b, g, r])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Define Target: Orange/Yellow/Brown tones
    # OpenCV Hue [0, 179]. Orange is ~10-25. Yellow ~25-35.
    # Brown is just Dark Orange.
    mask_orange = cv2.inRange(hsv, np.array([5, 30, 30]), np.array([40, 255, 255]))
    
    # Define Target: Semi-Transparent (The Aura/Edges)
    # Don't touch fully opaque armor (Alpha=255)
    # But some opaque parts might be the magic circle?
    # Let's be safe: Only touch pixels with Alpha < 250 OR very low value (dark brown)?
    # Let's try Alpha < 250 first.
    mask_trans = (a < 252) & (a > 0)
    
    # Combined Mask
    target_mask = (mask_orange > 0) & mask_trans
    
    # Shift Hue to Purple (approx 135-145 in OpenCV)
    # Set Hue to 140
    # Boost Saturation?
    
    h[target_mask] = 140 # Purple
    s[target_mask] = np.clip(s[target_mask] + 50, 0, 255) # Boost saturation
    
    # Reconstruct
    hsv_new = cv2.merge([h, s, v])
    bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    
    # Restore Alpha
    b_new, g_new, r_new = cv2.split(bgr_new)
    
    # Update only targeted pixels in original image channels?
    # Actually, we rebuilt the whole image.
    # But we only modified H/S where mask was true.
    # But converting back/forth might shift other colors slightly due to precision?
    # Safer to copy back only targeted pixels.
    
    b[target_mask] = b_new[target_mask]
    g[target_mask] = g_new[target_mask]
    r[target_mask] = r_new[target_mask]
    
    rgba_new = cv2.merge([b, g, r, a])
    
    cv2.imwrite(output_path, rgba_new)
    print(f"Purify Complete: {output_path}")

purify_aura("public/assets/dark_deity_unit.png", "public/assets/dark_deity_unit.png")
