import cv2
import numpy as np
import os

def process_icon_v2(input_name, output_name):
    base_dir = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/"
    input_path = os.path.join(base_dir, input_name)
    output_path = os.path.join(base_dir, output_name)
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Not found {input_name}")
        return

    # 1. Inspect Alpha to Crop Bounding Box
    if img.shape[2] == 4:
        alpha = img[:,:,3]
        coords = cv2.findNonZero(alpha)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            # Crop to content
            crop = img[y:y+h, x:x+w]
        else:
            crop = img
    else:
        crop = img
        b,g,r = cv2.split(crop)
        alpha = np.ones_like(b) * 255
        crop = cv2.merge([b,g,r,alpha])

    # 2. Resize to 128x128 (Force Stretch to Square)
    target_size = 128
    resized = cv2.resize(crop, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)
    
    # 3. Create Circle Mask
    mask = np.zeros((target_size, target_size), dtype=np.uint8)
    cv2.circle(mask, (target_size//2, target_size//2), target_size//2, 255, -1)
    
    # 4. Apply Mask
    b,g,r,a = cv2.split(resized)
    final_a = cv2.bitwise_and(a, mask)
    final_img = cv2.merge([b,g,r,final_a])
    
    cv2.imwrite(output_path, final_img)
    print(f"Saved {output_name}")

process_icon_v2("element_fire_v4.png", "element_fire_circle.png")
process_icon_v2("element_water.png", "element_water_circle.png")
process_icon_v2("element_electric.png", "element_electric_circle.png")
