
import cv2
import numpy as np

def ultimate_white_nuke():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Ultimate Nuke of Bright Low-Sat areas from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
    
    h, w = img.shape[:2]
    
    # ROI: Right Half (Where the stubborn white blob is)
    # x > w * 0.5
    roi_mask = np.zeros((h, w), dtype=np.uint8)
    roi_mask[:, int(w*0.5):] = 255
    
    # Analyze HSV
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    s = hsv[:, :, 1]
    
    # Condition: Bright (V > 150) AND Low-Med Saturation (S < 90)
    # S ranges 0-255. 90 is ~35%.
    # Gold Castle (S ~ 255) is Safe.
    # Green Leaves (S ~ ?) High.
    # Pale Yellow / White (S < 90).
    bad_mask = (v > 150) & (s < 90)
    bad_mask = bad_mask.astype(np.uint8) * 255
    
    # Intersect with ROI (Right Half)
    final_removal = cv2.bitwise_and(bad_mask, roi_mask)
    
    # Apply Alpha 0
    img[final_removal > 0, 3] = 0
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Ultimate Nuke)")

ultimate_white_nuke()
