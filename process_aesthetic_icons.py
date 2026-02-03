
import cv2
import numpy as np

def process_aesthetic_icons():
    icons = [
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/aesthetic_stat_attack_raw_1769886510308.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_attack_v2.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/aesthetic_stat_defense_raw_1769886525964.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_defense_v2.png"
        },
        {
            "src": "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/aesthetic_stat_overdrive_raw_1769886537587.png",
            "out": "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/stat_overdrive_v2.png"
        }
    ]

    for item in icons:
        img = cv2.imread(item["src"], cv2.IMREAD_UNCHANGED)
        if img is None:
            continue

        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # Better extraction for objects on white
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        
        # Invert and threshold to find the object
        _, mask = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY_INV)
        
        # Clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Smooth edges
        mask = cv2.GaussianBlur(mask, (3,3), 0)
        
        img[:, :, 3] = mask
        
        # Tight crop
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Add small padding
            padding = 10
            y1 = max(0, y - padding)
            y2 = min(img.shape[0], y + h + padding)
            x1 = max(0, x - padding)
            x2 = min(img.shape[1], x + w + padding)
            
            cropped = img[y1:y2, x1:x2]
            
            # Make square
            side = max(cropped.shape[0], cropped.shape[1])
            square = np.zeros((side, side, 4), dtype=np.uint8)
            oy = (side - cropped.shape[0]) // 2
            ox = (side - cropped.shape[1]) // 2
            square[oy:oy+cropped.shape[0], ox:ox+cropped.shape[1]] = cropped
            
            # Resize
            final = cv2.resize(square, (128, 128), interpolation=cv2.INTER_AREA)
            cv2.imwrite(item["out"], final)

if __name__ == "__main__":
    process_aesthetic_icons()
