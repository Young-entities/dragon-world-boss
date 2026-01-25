import cv2
import numpy as np

def surgical_v25_connected_white(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. IDENTIFY CONNECTED BACKGROUND (Flood Fill)
    # We use a high tolerance (50) to swallow the white borders and shadows
    # but starting from the corners so we don't hit the internal face.
    temp_img = img.copy()
    mask = np.zeros((h+2, w+2), np.uint8)
    fill_color = (255, 0, 255) # Magenta
    
    # Corners
    pts = [(0,0), (w-1,0), (0,h-1), (w-1,h-1), (w//2, 0), (0, h//2)]
    for pt in pts:
        cv2.floodFill(temp_img, mask, pt, fill_color, (50, 50, 50), (50, 50, 50))
    
    # 2. IDENTIFY INTERNAL WHITE GAPS (HSV)
    # This targets the white blocks between dragons
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Internal white = Low saturation and High value
    internal_white = (s < 30) & (v > 210)
    
    # 3. FACIAL PROTECTION
    # Protect the face region from internal white cleanup
    shield = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(shield, (654, 255), 100, 255, -1)
    
    # 4. FINAL ASSEMBLY
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Transparency rule 1: Connected background (Corner FloodFilled)
    is_outer_bg = (temp_img[:,:,0] == 255) & (temp_img[:,:,1] == 0) & (temp_img[:,:,2] == 255)
    alpha[is_outer_bg] = 0
    # Transparency rule 2: Internal white gaps (if not protected)
    alpha[internal_white & (shield == 0)] = 0
    
    rgba[:,:,3] = alpha
    
    # 5. PHYSICAL CROP
    # Crop to remove AI borders and bottom black footer
    rgba = rgba[18:h-45, 18:w-18]
    
    cv2.imwrite(output_path, rgba)
    print(f"Connected white dissolved: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_fm14x0fm14x0fm14.png"
surgical_v25_connected_white(source, "public/assets/water_deity_unit_final.png")
