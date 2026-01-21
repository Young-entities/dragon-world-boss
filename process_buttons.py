
import cv2
import numpy as np
import os
import glob
import shutil

source_dir = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae"
dest_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def process_button(pattern, out_name):
    files = glob.glob(os.path.join(source_dir, f"{pattern}*.png"))
    if not files:
        print(f"No file found for {pattern}")
        return
    
    src_path = max(files, key=os.path.getmtime)
    print(f"Processing {src_path}")
    
    img = cv2.imread(src_path)
    if img is None:
        print("Failed to read")
        return
    
    # Convert to BGRA
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Create mask where pixels are very dark (black background)
    # Sum of RGB channels < threshold means it's black
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Black pixels (< 20) become transparent
    mask = gray < 20
    img_rgba[mask, 3] = 0
    
    out_path = os.path.join(dest_dir, out_name)
    cv2.imwrite(out_path, img_rgba)
    print(f"Saved to {out_path}")

process_button("btn_final_blue", "btn_blue.png")
process_button("btn_final_green", "btn_green.png")
process_button("btn_final_red_v2", "btn_red.png")

print("Done!")
