
import cv2
import numpy as np
import os
import glob

source_dir = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae"
dest_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def process_button(pattern, out_name):
    # Find the latest file matching pattern
    files = glob.glob(os.path.join(source_dir, f"{pattern}*.png"))
    if not files:
        print(f"No file found for {pattern}")
        return
    
    # Get most recent
    src_path = max(files, key=os.path.getmtime)
    print(f"Processing {src_path}")
    
    img = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Failed to read")
        return
    
    # Add alpha if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    h, w = img.shape[:2]
    
    # Remove black background using flood fill from corners
    # This is cleaner than threshold since it follows connected regions
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Flood fill from all 4 corners with tolerance
    tolerance = (30, 30, 30, 255)
    cv2.floodFill(img, mask, (0, 0), (0, 0, 0, 0), tolerance, tolerance, cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(img, mask, (w-1, 0), (0, 0, 0, 0), tolerance, tolerance, cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(img, mask, (0, h-1), (0, 0, 0, 0), tolerance, tolerance, cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(img, mask, (w-1, h-1), (0, 0, 0, 0), tolerance, tolerance, cv2.FLOODFILL_FIXED_RANGE)
    
    # Save
    out_path = os.path.join(dest_dir, out_name)
    cv2.imwrite(out_path, img)
    print(f"Saved to {out_path}")

process_button("btn_blue_clean", "btn_blue.png")
process_button("btn_green_clean", "btn_green.png")
process_button("btn_red_clean", "btn_red.png")

print("Done!")
