import cv2
import numpy as np
import os

def process_icon_v4(input_name, output_name, scale=1.0):
    base_dir = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/"
    input_path = os.path.join(base_dir, input_name)
    output_path = os.path.join(base_dir, output_name)
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Not found {input_name}")
        return

    # 1. Crop to Content
    if img.shape[2] == 4:
        alpha = img[:,:,3]
        coords = cv2.findNonZero(alpha)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            crop = img[y:y+h, x:x+w]
        else:
            crop = img
    else:
        crop = img
        b,g,r = cv2.split(crop)
        alpha = np.ones_like(b) * 255
        crop = cv2.merge([b,g,r,alpha])

    # 2. Setup Canvas 128x128
    canvas_size = 128
    
    # Base Content Size is 116 (from V3). Apply Scale.
    base_size = 116
    content_size = int(base_size * scale)
    
    # Resize Crop to Content Size (Force Stretch to Square)
    resized_content = cv2.resize(crop, (content_size, content_size), interpolation=cv2.INTER_LANCZOS4)
    
    # 3. Paste into Center
    bg = np.zeros((canvas_size, canvas_size, 4), dtype=np.uint8)
    offset = (canvas_size - content_size) // 2
    bg[offset:offset+content_size, offset:offset+content_size] = resized_content
    
    # 4. Circle Mask
    mask = np.zeros((canvas_size, canvas_size), dtype=np.uint8)
    cv2.circle(mask, (canvas_size//2, canvas_size//2), canvas_size//2, 255, -1)
    
    # Apply Mask
    b,g,r,a = cv2.split(bg)
    final_a = cv2.bitwise_and(a, mask)
    final_img = cv2.merge([b,g,r,final_a])
    
    cv2.imwrite(output_path, final_img)
    print(f"Saved {output_name} with scale {scale}")

# Adjust Scales to balance visual weight
# Electric looks biggest (Yellow/Bright) -> Reduce scale
process_icon_v4("element_electric.png", "element_electric_circle.png", scale=0.9)

# Water looks okay (Blue/Dark) -> Keep standard
process_icon_v4("element_water.png", "element_water_circle.png", scale=1.0)

# Fire looks smallest (Red/Complex shape) -> Increase scale slightly
process_icon_v4("element_fire_v4.png", "element_fire_circle.png", scale=1.05)
