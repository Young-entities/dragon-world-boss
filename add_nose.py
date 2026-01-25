import cv2
import numpy as np

def add_anime_nose(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return

    # Current image is (approx 600x900)
    h, w = img.shape[:2]
    
    # Coordinates for the nose in the Lanczos-upscaled image:
    # Based on the crop coordinates (mouth was at 153, 453)
    # Nose should be slightly above the mouth area.
    nose_y, nose_x = 142, 453 
    
    # 1. Define the nose color (slightly darker skin tone)
    # Sample skin tone near the nose area
    skin_sample = img[nose_y:nose_y+5, nose_x-10:nose_x+10, :3]
    base_color = np.median(skin_sample.reshape(-1, 3), axis=0)
    # Make it 20% darker for the shadow/line
    nose_color = (base_color * 0.8).astype(np.uint8).tolist()
    
    # 2. Draw a subtle anime nose line
    # A tiny diagonal tick or a small dot is classic for this style
    # Let's draw a very small 2-pixel subtle vertical line
    cv2.line(img, (nose_x, nose_y), (nose_x + 1, nose_y + 2), nose_color, 1)
    
    # Soften it so it doesn't look like a pixel error
    nose_roi = img[nose_y-2:nose_y+5, nose_x-2:nose_x+3]
    img[nose_y-2:nose_y+5, nose_x-2:nose_x+3] = cv2.GaussianBlur(nose_roi, (3,3), 0)

    cv2.imwrite(output_path, img)
    print(f"Elegant anime nose added: {output_path}")

add_anime_nose("public/assets/water_deity_unit_final.png", "public/assets/water_deity_unit_final.png")
