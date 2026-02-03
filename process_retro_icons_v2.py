
import cv2
import numpy as np

def process_retro_stat_icons_v2():
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

        # 1. Convert to grayscale to find the white background
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        
        # 2. Find the object (the crimson rounded square)
        # Instead of global INV threshold which kills the white text, 
        # we threshold to find the darker parts + colored parts, 
        # but the most robust way is to find the largest contour that isn't the whole image.
        
        # Background is white (255). Let's threshold to find anything NOT white.
        _, mask = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY_INV)
        
        # 3. Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: continue
        
        # Get the largest contour (the button)
        cnt = max(contours, key=cv2.contourArea)
        
        # 4. Create a solid mask for the button shape
        # This preserves EVERYTHING inside the button boundary, including the white text.
        button_mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(button_mask, [cnt], -1, 255, -1)
        
        # 5. Apply the mask as the alpha channel
        img[:, :, 3] = button_mask
        
        # 6. Crop to the button
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = img[y:y+h, x:x+w]
        
        # 7. Make square and resize
        side = max(w, h)
        square = np.zeros((side, side, 4), dtype=np.uint8)
        dy = (side - h) // 2
        dx = (side - w) // 2
        square[dy:dy+h, dx:dx+w] = cropped
        
        final = cv2.resize(square, (128, 128), interpolation=cv2.INTER_AREA)
        cv2.imwrite(item["out"], final)
        print(f"Reprocessed {item['out']}")

if __name__ == "__main__":
    process_retro_stat_icons_v2()
