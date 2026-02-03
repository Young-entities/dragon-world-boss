
import cv2
import numpy as np

def crop_to_target(input_path, output_path, target_w, target_h):
    print(f"Cropping {input_path} to {target_w}x{target_h}")
    
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Image not found.")
        return

    h, w = img.shape[:2]
    
    # We want to match target_w x target_h
    # Assuming width is matching (1024), crop height.
    
    if w != target_w:
        # Resize width to match target?
        scale = target_w / w
        new_w = target_w
        new_h_temp = int(h * scale)
        img = cv2.resize(img, (new_w, new_h_temp), interpolation=cv2.INTER_AREA)
        h, w = img.shape[:2]
    
    if h > target_h:
        # Crop center vertical
        start_y = (h - target_h) // 2
        img = img[start_y : start_y + target_h, :]
        print(f"Cropped vertical center.")
    elif h < target_h:
        print("Image too short. Padding?")
        # Pad?
        # Azaerth BG is 1024x681. Our BG is 1024x1024. So we crop.
        pass

    cv2.imwrite(output_path, img)
    print(f"Saved to {output_path}")

target_w, target_h = 1024, 681
path = "public/assets/celestial_bg.png"
crop_to_target(path, path, target_w, target_h)
