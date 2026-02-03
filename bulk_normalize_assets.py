
import cv2
import os
import numpy as np

def normalize_to_ratio(img, target_w, target_h, mode="pad"):
    h, w = img.shape[:2]
    target_aspect = target_w / target_h
    current_aspect = w / h
    
    if mode == "pad":
        # Ensure we fit inside target aspect, then resize to exact pixels
        if current_aspect < target_aspect:
            # Too narrow, pad sides
            new_w = int(h * target_aspect)
            pad_total = new_w - w
            pad_left = pad_total // 2
            pad_right = pad_total - pad_left
            img = cv2.copyMakeBorder(img, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=(0,0,0,0))
        elif current_aspect > target_aspect:
            # Too wide, pad top/bottom
            new_h = int(w / target_aspect)
            pad_total = new_h - h
            pad_top = pad_total // 2
            pad_bot = pad_total - pad_top
            img = cv2.copyMakeBorder(img, pad_top, pad_bot, 0, 0, cv2.BORDER_CONSTANT, value=(0,0,0,0))
    elif mode == "crop":
        # Crop centers to match aspect
        if current_aspect > target_aspect:
            # Too wide, crop sides
            new_w = int(h * target_aspect)
            diff = w - new_w
            x_start = diff // 2
            img = img[:, x_start:x_start+new_w]
        elif current_aspect < target_aspect:
            # Too tall, crop top/bottom
            new_h = int(w / target_aspect)
            diff = h - new_h
            y_start = diff // 2
            img = img[y_start:y_start+new_h, :]
            
    # Final resize to exact target pixels
    return cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

def run_bulk_normalize():
    # Targets
    UNIT_SIZE = (1200, 896)
    BG_SIZE = (1248, 832)
    ICON_SIZE = (992, 992)
    
    # Asset lists from monsters.js
    units = [
        "public/assets/overlord_absolute_final.png",
        "public/assets/water_deity_unit_final.png",
        "public/assets/electric_god_unit_clean.png",
        "public/assets/water_god_unit_clean.png",
        "public/assets/dark_deity_unit_v4.png",
        "public/assets/fire_empress_unit.png",
        "public/assets/water_oracle_unit.png",
        "public/assets/celestial_valkyrie.png"
    ]
    bgs = [
        "public/assets/water_deity_card_bg.png",
        "public/assets/electric_bg_final.png",
        "public/assets/water_elara_bg.png",
        "public/assets/dark_void_bg.png",
        "public/assets/fire_empress_bg.png",
        "public/assets/water_oracle_bg.png",
        "public/assets/celestial_bg.png"
    ]
    icons = [
        "public/assets/overlord_face_crop.png",
        "public/assets/water_deity_face_crop.png",
        "public/assets/electric_god_icon.png",
        "public/assets/water_god_icon.png",
        "public/assets/dark_deity_icon.png",
        "public/assets/fire_empress_icon.png",
        "public/assets/water_oracle_icon.png",
        "public/assets/celestial_icon.png"
    ]
    
    print("Normalizing Units...")
    for f in units:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            if img is not None:
                img = normalize_to_ratio(img, UNIT_SIZE[0], UNIT_SIZE[1], "pad")
                cv2.imwrite(f, img)
                print(f"  Processed {f}")
                
    print("Normalizing Backgrounds...")
    for f in bgs:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            if img is not None:
                img = normalize_to_ratio(img, BG_SIZE[0], BG_SIZE[1], "crop")
                cv2.imwrite(f, img)
                print(f"  Processed {f}")
                
    print("Normalizing Icons...")
    for f in icons:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            if img is not None:
                img = normalize_to_ratio(img, ICON_SIZE[0], ICON_SIZE[1], "crop")
                cv2.imwrite(f, img)
                print(f"  Processed {f}")

run_bulk_normalize()
