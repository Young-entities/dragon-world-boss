import cv2
import numpy as np
import glob
import os

def diag_spear_pixels():
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Analyzing source: {latest_file}")
    
    img = cv2.imread(latest_file)
    b, g, r = cv2.split(img)
    h, w = img.shape[:2]
    
    # Define a small diagnostic box on the spear tip edge
    # (Approximate location based on previous masks)
    # y~80%, x~20%
    y0, y1 = int(h*0.80), int(h*0.82)
    x0, x1 = int(w*0.20), int(w*0.22)
    
    crop_b = b[y0:y1, x0:x1]
    crop_g = g[y0:y1, x0:x1]
    crop_r = r[y0:y1, x0:x1]
    
    print("-" * 30)
    print("Sampling Pixels from Spear Tip Region:")
    print("Format: (R, G, B) | Hex | Saturation")
    
    count = 0
    for i in range(crop_b.shape[0]):
        for j in range(crop_b.shape[1]):
            B, G, R = int(crop_b[i,j]), int(crop_g[i,j]), int(crop_r[i,j])
            
            # Simple Brightness
            luma = (R+G+B)//3
            
            # Only look at Dark pixels (Outline candidates)
            if luma < 80 and luma > 10:
                sat = max(R,G,B) - min(R,G,B)
                hex_col = f"#{R:02x}{G:02x}{B:02x}"
                print(f"Px: ({R:3}, {G:3}, {B:3}) | {hex_col} | Sat: {sat}")
                count += 1
                if count > 20: break
        if count > 20: break
    
    print(f"Sampled {count} dark pixels.")
    print("-" * 30)

diag_spear_pixels()
