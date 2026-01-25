import cv2
import numpy as np
import glob
import os

def surgical_v105_black_ops(output_path):
    # 1. Find the newest Gemini PNG (Look in parent dir too)
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files:
        print("No Gemini_*.png files found in . or ..!")
        return
        
    # Sort by modification time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Detected latest source image: {latest_file}")
    
    img = cv2.imread(latest_file)
    if img is None:
        print("Could not read file.")
        return

    # 1. Setup BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    b, g, r = cv2.split(img)
    
    # 2. Check for Black Background
    # Sample corner pixels
    corner_avg = np.mean(img[0:10, 0:10])
    print(f"Corner Average Brightness: {corner_avg}")
    
    if corner_avg > 50:
        print("WARNING: This image does not seem to have a black background! Aborting safety check.")
        # Proceeding anyway just in case the check is wrong, but warning user.
        # Use simple "Dark" threshold.
        
    # 3. EXTRACTION LOGIC (The Easy Way)
    # Background is BLACK. (0,0,0)
    # Unit is NOT Black.
    
    # Calculate total brightness
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    
    # Threshold: Anything darker than (10,10,10) is background
    is_bg = brightness < 30
    
    # Create Mask
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 4. POLISH (Remove Black Fringe)
    # Simply eroding by 1px cleans up the anti-aliased black edge.
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=1)
    
    # 5. Clean Color Channels
    # Where alpha is 0, set RGB to 0 (cleanliness)
    rgba[:,:,3] = alpha
    rgba[alpha == 0, :3] = 0
    
    cv2.imwrite(output_path, rgba)
    print(f"Black Ops Extraction Complete: {output_path}")

surgical_v105_black_ops("public/assets/water_deity_unit_final.png")
