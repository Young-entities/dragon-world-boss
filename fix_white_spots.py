
import cv2
import numpy as np

def fix_white_spots():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Removing residual white spots from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
        
    # Check if we have alpha
    if img.shape[2] < 4:
        print("Image has no alpha channel, adding one")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Safe Zone Radius (Protect Face/Eyes)
    # Assume face is roughly central. Radius 15% of width?
    safe_radius = int(w * 0.15)
    
    # White Threshold
    # Pixels close to (255, 255, 255)
    lower_white = np.array([230, 230, 230, 0], dtype=np.uint8)
    upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)
    
    # Create White Mask
    white_mask = cv2.inRange(img, lower_white, upper_white)
    
    # Create Safe Zone Mask (Black Circle on White BG)
    safe_mask = np.ones((h, w), dtype=np.uint8) * 255
    cv2.circle(safe_mask, (cx, int(cy*0.8)), safe_radius, 0, -1) # Offset cy slightly up for eyes
    
    # Target Mask: White Pixels AND Outside Safe Zone
    # (white_mask > 0) AND (safe_mask > 0)
    target_mask = cv2.bitwise_and(white_mask, safe_mask)
    
    # Apply Alpha 0
    img[target_mask > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Removed White Spots)")

fix_white_spots()
