import cv2
import numpy as np

def update_bg():
    bg_path = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/fire_card_bg_v5_1769713242668.png"
    output_path = "public/assets/fire_empress_bg.png"
    
    bg = cv2.imread(bg_path)
    if bg is None:
        print("BG load failed")
        return
        
    # Crop Borders (Remove Gold Frame and Icons)
    border_crop = 75
    h_raw, w_raw = bg.shape[:2]
    bg = bg[border_crop:h_raw-border_crop, border_crop:w_raw-border_crop]
    
    target_w = 900
    target_h = 600
    
    h_b, w_b = bg.shape[:2]
    target_ratio = target_w / target_h
    bg_ratio = w_b / h_b
    
    if bg_ratio > target_ratio:
        new_h_b = h_b
        new_w_b = int(h_b * target_ratio)
        cx = w_b // 2
        bg_cropped = bg[:, cx-new_w_b//2 : cx+new_w_b//2]
    else:
        new_w_b = w_b
        new_h_b = int(w_b / target_ratio)
        cy = h_b // 2
        bg_cropped = bg[cy-new_h_b//2 : cy+new_h_b//2, :]
        
    bg_final = cv2.resize(bg_cropped, (target_w, target_h), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, bg_final)
    print(f"Updated BG Saved: {output_path}")

update_bg()
