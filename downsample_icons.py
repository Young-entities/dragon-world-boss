
import cv2
import numpy as np

def downsample_icons():
    print("Downsampling huge icons to ~54px for crisp rendering at small sizes...")
    
    files = [
        "public/assets/element_holy.png",
        "public/assets/element_holy_circle.png",
        "public/assets/element_dark.png",
        "public/assets/element_dark_circle.png"
    ]
    
    TARGET_SIZE = 54
    
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        
        # Only downsample if huge
        if w > 100:
            print(f"Downsampling {f} ({w}x{h}) -> {TARGET_SIZE}x{TARGET_SIZE}")
            
            # Interpolation Area is best for shrinking
            new_img = cv2.resize(img, (TARGET_SIZE, TARGET_SIZE), interpolation=cv2.INTER_AREA)
            
            cv2.imwrite(f, new_img)

downsample_icons()
