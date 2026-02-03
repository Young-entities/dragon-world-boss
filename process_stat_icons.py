
import cv2
import numpy as np
import os

def process_stat_icons():
    icons = [
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_icon_attack_raw_1769886417826.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_attack.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_icon_defense_raw_1769886429820.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_defense.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/stat_icon_overdrive_raw_1769886442206.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_overdrive.png"
        }
    ]

    for item in icons:
        img = cv2.imread(item["src"], cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Failed to load {item['src']}")
            continue

        # If it has 3 channels, add alpha
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # Convert to grayscale to find white background
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        
        # Mask out anything that is perfect white or very close to it
        _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
        
        # Also find the main circle using contours to be precise
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            
            # Create a circular mask
            circle_mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.drawContours(circle_mask, [c], -1, 255, -1)
            
            # Combine masks
            final_mask = cv2.bitwise_and(mask, circle_mask)
            
            # Apply alpha
            img[:, :, 3] = final_mask
            
            # Crop to the circle
            res = img[y:y+h, x:x+w]
            
            # Resize to 128x128
            res = cv2.resize(res, (128, 128), interpolation=cv2.INTER_AREA)
            
            cv2.imwrite(item["out"], res)
            print(f"Saved {item['out']}")

if __name__ == "__main__":
    process_stat_icons()
