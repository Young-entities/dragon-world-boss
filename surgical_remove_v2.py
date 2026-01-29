import cv2
import numpy as np

def surgical_v2(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # ROI: Top 120 pixels
    roi = img[0:120, :]
    
    # Text Masking Strategy:
    # 1. Mask Gold
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_gold = np.array([10, 80, 80])
    upper_gold = np.array([40, 255, 255])
    mask_gold = cv2.inRange(hsv, lower_gold, upper_gold)
    
    # 2. Find Bounds of Gold (The Text Area)
    # Dilate gold to connect letters
    kernel = np.ones((5,5), np.uint8)
    gold_dilated = cv2.dilate(mask_gold, kernel, iterations=3)
    
    contours, _ = cv2.findContours(gold_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mask_to_inpaint = np.zeros(roi.shape[:2], dtype=np.uint8)
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Filter small noise
        if w > 20 and h > 10:
            # Draw rectangle over the text area + padding
            # This covers outline and shadow
            cv2.rectangle(mask_to_inpaint, (x-5, y-5), (x+w+5, y+h+5), 255, -1)
            
    # 3. Inpaint
    roi_inpainted = cv2.inpaint(roi, mask_to_inpaint, 3, cv2.INPAINT_TELEA) # or NS
    img[0:120, :] = roi_inpainted
    
    # 4. Transparency (Reuse logic)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask_bg = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    mask_fg = cv2.bitwise_not(mask_bg)
    
    h, w = img.shape[:2]
    prot = np.zeros((h,w), np.uint8)
    cv2.ellipse(prot, (w//2, h//2+20), (int(w*0.4), int(h*0.45)), 0, 0, 360, 255, -1)
    
    alpha = cv2.bitwise_or(mask_fg, prot)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V2 Complete: {output_path}")

surgical_v2("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769654171456.png", "public/assets/dark_deity_unit.png")
