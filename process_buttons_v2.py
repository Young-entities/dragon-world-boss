
import os
import cv2
import numpy as np

# Paths
source_dir = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae"
dest_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def process_button_aggressive(filename, color_name):
    # Find the latest file matching the pattern
    files = [f for f in os.listdir(source_dir) if f.startswith(filename) and f.endswith(".png")]
    if not files:
        print(f"No file found for {filename}")
        return

    src_path = os.path.join(source_dir, files[-1])
    img = cv2.imread(src_path)
    
    # Force add alpha
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Aggressive Black Removal
    # Scan from corners to find background color
    # Top-Left Pixel
    bg_color = img[0,0]
    print(f"File {filename} corner color: {bg_color}")
    
    # Create mask where pixels are close to black (or corner color)
    # Threshold < 40 for RGB
    mask = np.all(img[:, :, :3] < 45, axis=2)
    
    # Set those pixels to transparent
    img[mask] = [0, 0, 0, 0]
    
    # Crop to content
    # Find non-transparent pixels
    alpha = img[:, :, 3]
    coords = cv2.findNonZero(alpha)
    x, y, w, h = cv2.boundingRect(coords)
    
    cropped = img[y:y+h, x:x+w]
    
    out_path = os.path.join(dest_dir, f"btn_{color_name}.png")
    cv2.imwrite(out_path, cropped)
    print(f"Saved {out_path}")

# Re-process all, especially green
process_button_aggressive("ui_btn_blue", "blue")
process_button_aggressive("ui_btn_green", "green")
process_button_aggressive("ui_btn_red", "red")
