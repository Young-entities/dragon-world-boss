
import cv2
import numpy as np
import os

asset_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def clean_lava_aggressive(name):
    path = os.path.join(asset_dir, f"btn_{name}_exact.png")
    if not os.path.exists(path):
        return
        
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    # Ensure alpha
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
    h, w = img.shape[:2]
    
    # Create Mask
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Radius 20 was okay, but let's INSET the mask.
    # New Radius 22? And inset the rect by 2 pixels.
    inset = 4
    radius = 18
    
    # Draw smaller rounded rect
    # Top-Left
    cv2.circle(mask, (radius+inset, radius+inset), radius, (255), -1)
    # Top-Right
    cv2.circle(mask, (w-radius-inset, radius+inset), radius, (255), -1)
    # Bottom-Left
    cv2.circle(mask, (radius+inset, h-radius-inset), radius, (255), -1)
    # Bottom-Right
    cv2.circle(mask, (w-radius-inset, h-radius-inset), radius, (255), -1)
    
    # Central Rects
    cv2.rectangle(mask, (radius+inset, inset), (w-radius-inset, h-inset), (255), -1)
    cv2.rectangle(mask, (inset, radius+inset), (w-inset, h-radius-inset), (255), -1)
    
    # Apply
    # We combine existing alpha with new mask?
    # img[:,:,3] = cv2.bitwise_and(img[:,:,3], mask)
    # Just replace alpha where mask is 0
    
    # Find where mask is 0
    img[mask == 0] = [0, 0, 0, 0]
    
    # Save
    cv2.imwrite(path, img)
    print(f"Aggressively cleaned {name}")

clean_lava_aggressive("blue")
clean_lava_aggressive("green")
clean_lava_aggressive("red")
