
import cv2
import numpy as np

def process_retro_stat_icons():
    icons = [
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_atk_up_raw_1769886879980.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_attack_retro.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_def_up_raw_1769886894762.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_defense_retro.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_od_up_raw_1769886908967.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_overdrive_retro.png"
        }
    ]

    for item in icons:
        img = cv2.imread(item["src"], cv2.IMREAD_UNCHANGED)
        if img is None: continue

        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
        
        # Find the main rounded square
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Create a tighter mask based on the actual bounding box
            # But the AI sometimes generates shadows outside. 
            # We want to keep the rounded square shape.
            
            # Simple crop to bounding box
            cropped = img[y:y+h, x:x+w]
            
            # Apply alpha based on white background removal for this crop
            c_gray = cv2.cvtColor(cropped, cv2.COLOR_BGRA2GRAY)
            _, c_mask = cv2.threshold(c_gray, 252, 255, cv2.THRESH_BINARY_INV)
            
            # Add back alpha
            cropped[:, :, 3] = c_mask
            
            # Resize
            final = cv2.resize(cropped, (128, 128), interpolation=cv2.INTER_AREA)
            cv2.imwrite(item["out"], final)

if __name__ == "__main__":
    process_retro_stat_icons()
