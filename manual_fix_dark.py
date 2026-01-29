import cv2
import numpy as np

def fix_dark_unit(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # 1. Remove "13-STAR RARITY" Text
    # ROI: Top 100 pixels
    roi = img[0:100, :]
    
    # Text is Gold/Yellow/Orange
    # HSV Range
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Gold/Yellow: H=15-35 approx
    lower_gold = np.array([10, 100, 100])
    upper_gold = np.array([40, 255, 255])
    
    mask_text = cv2.inRange(hsv_roi, lower_gold, upper_gold)
    
    # Also mask dark outlines of text? (Black/Dark Brown)
    # Text has distinct outline.
    
    # Dilate mask to cover edges
    kernel = np.ones((3,3), np.uint8)
    mask_text = cv2.dilate(mask_text, kernel, iterations=2)
    
    # Inpaint
    roi_inpainted = cv2.inpaint(roi, mask_text, 3, cv2.INPAINT_TELEA)
    img[0:100, :] = roi_inpainted

    # 2. Change White Background to Green (0, 255, 0)
    # Threshold white
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # White is Low Saturation, High Value
    lower_white = np.array([0, 0, 240])
    upper_white = np.array([180, 50, 255])
    
    mask_bg = cv2.inRange(hsv, lower_white, upper_white)
    
    # Set BG to Green
    img[mask_bg > 0] = [0, 255, 0] # BGR
    
    cv2.imwrite(output_path, img)
    print(f"Fixed (No Text, Green BG): {output_path}")

fix_dark_unit("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769654171456.png", "public/assets/dark_deity_green.png")
