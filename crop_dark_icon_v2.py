import cv2

def crop_icon_center(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    # Center Crop for Face
    # 1024x1024 input.
    # Face approx at x=512, y=350. Size 256x256.
    
    x_center = 512
    y_center = 350
    crop_size = 300 # Slightly larger to catch horns/mask
    
    x1 = max(0, x_center - crop_size//2)
    y1 = max(0, y_center - crop_size//2)
    x2 = min(img.shape[1], x1 + crop_size)
    y2 = min(img.shape[0], y1 + crop_size)
    
    crop = img[y1:y2, x1:x2]
    
    # Resize to standard icon size (e.g. 128 or 256)
    # Most icons are displayed small. 
    # Resize to 200x200
    crop = cv2.resize(crop, (200, 200), interpolation=cv2.INTER_AREA)
    
    cv2.imwrite(output_path, crop)
    print(f"Created Icon: {output_path}")

crop_icon_center("public/assets/dark_deity_unit.png", "public/assets/dark_deity_icon.png")
