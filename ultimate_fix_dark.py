import cv2
import numpy as np

def fix_and_transparency(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # 1. Remove "13-STAR RARITY" Text via Inpainting
    roi = img[0:100, :]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Gold Text Mask
    lower_gold = np.array([10, 100, 100])
    upper_gold = np.array([40, 255, 255])
    mask_text = cv2.inRange(hsv_roi, lower_gold, upper_gold)
    
    # Dilate
    kernel = np.ones((3,3), np.uint8)
    mask_text = cv2.dilate(mask_text, kernel, iterations=2)
    
    # Inpaint
    roi_inpainted = cv2.inpaint(roi, mask_text, 3, cv2.INPAINT_TELEA)
    img[0:100, :] = roi_inpainted

    # 2. Make Background Transparent
    # Threshold White
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask_bg = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    mask_fg = cv2.bitwise_not(mask_bg)
    
    # Protect Center
    h, w = img.shape[:2]
    prot = np.zeros((h,w), np.uint8)
    cv2.ellipse(prot, (w//2, h//2+20), (int(w*0.4), int(h*0.45)), 0, 0, 360, 255, -1)
    
    alpha = cv2.bitwise_or(mask_fg, prot)
    
    # Create RGBA
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Fixed & Transparent: {output_path}")

fix_and_transparency("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769654171456.png", "public/assets/dark_deity_unit.png")
