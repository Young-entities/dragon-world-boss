
import cv2
import numpy as np

def standardize_assets():
    target_aspect = 1.34 # W / H
    
    files = [
        ("public/assets/earth_minion.png", "pad"),
        ("public/assets/earth_tree_bg.png", "crop")
    ]
    
    print(f"Standardizing assets to Aspect Ratio {target_aspect:.2f}...")
    
    for fname, mode in files:
        img = cv2.imread(fname, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
            
        h, w = img.shape[:2]
        current_aspect = w / h
        print(f"{fname}: {w}x{h} ({current_aspect:.2f}) -> Mode: {mode}")
        
        if mode == "pad":
            # Unit: Pad Width to match aspect (don't crop unit)
            # Or Pad Height if too wide?
            if current_aspect < target_aspect:
                # Too Tall (Square). Need to Pad Width.
                new_w = int(h * target_aspect)
                pad_w = new_w - w
                pad_l = pad_w // 2
                pad_r = pad_w - pad_l
                
                # Use standard copyMakeBorder with TRANSPARENT border for Unit
                # Or just empty buffer?
                # Check channels
                if len(img.shape) == 2: # Gray
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
                elif img.shape[2] == 3: # BGR
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
                    
                # Pad
                img = cv2.copyMakeBorder(img, 0, 0, pad_l, pad_r, cv2.BORDER_CONSTANT, value=(0,0,0,0))
                print(f"  Padded to {img.shape[1]}x{img.shape[0]}")
                
            else:
                print("  Already wide enough?")
                
        elif mode == "crop":
            # Background: Crop to match aspect (don't add black bars)
            # Usually BG is square.
            if current_aspect < target_aspect:
                # Too Tall. Crop Height.
                new_h = int(w / target_aspect)
                diff = h - new_h
                y_start = diff // 2
                y_end = y_start + new_h
                
                img = img[y_start:y_end, :]
                print(f"  Cropped to {img.shape[1]}x{img.shape[0]}")
                
        cv2.imwrite(fname, img)

standardize_assets()
