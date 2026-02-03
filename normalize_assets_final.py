
import cv2
import numpy as np

def normalize_assets_final():
    # Target dimensions based on Overlord and Deity units
    TARGET_UNIT_W, TARGET_UNIT_H = 1200, 896 # 1.34 aspect
    TARGET_BG_W, TARGET_BG_H = 1248, 832    # 1.50 aspect
    TARGET_ICON_SIZE = 992                   # 1.00 aspect
    
    # 1. Standardize Unit (earth_minion.png) to 1200x896
    unit_src = "public/assets/earth_minion.png"
    img_unit = cv2.imread(unit_src, cv2.IMREAD_UNCHANGED)
    if img_unit is not None:
        # Resize/Pad to exactly 1200x896
        # Current is 1372x1024 (1.34)
        img_unit_resized = cv2.resize(img_unit, (TARGET_UNIT_W, TARGET_UNIT_H), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite("public/assets/earth_minion_final.png", img_unit_resized)
        print(f"Saved earth_minion_final.png: {TARGET_UNIT_W}x{TARGET_UNIT_H}")

    # 2. Standardize Background (earth_tree_bg.png) to 1248x832
    bg_src = "public/assets/earth_tree_bg.png"
    img_bg = cv2.imread(bg_src, cv2.IMREAD_UNCHANGED)
    if img_bg is not None:
        # Current is 1024x764 (1.34) - wait, checking check_all_dims output...
        # 1024x764 is 1.34. I need 1.50.
        # To get 1.50 from 1.34, I must crop height even more or pad width.
        # BG is better to crop. 
        h, w = img_bg.shape[:2]
        target_aspect = TARGET_BG_W / TARGET_BG_H # 1.5
        
        new_h = int(w / target_aspect)
        diff = h - new_h
        y_start = diff // 2
        y_end = y_start + new_h
        img_bg_cropped = img_bg[y_start:y_end, :]
        img_bg_resized = cv2.resize(img_bg_cropped, (TARGET_BG_W, TARGET_BG_H), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite("public/assets/earth_tree_bg_final.png", img_bg_resized)
        print(f"Saved earth_tree_bg_final.png: {TARGET_BG_W}x{TARGET_BG_H}")

    # 3. Create Square Icon (earth_icon.png) 992x992
    # Use the original unit image (which was 1024x1024 square before I padded it?)
    # Wait, I don't have the original 1:1 anymore? 
    # Yes I do, the earth_minion.png was square before Step 8468.
    # I can just take the padded version and crop the center square.
    if img_unit is not None:
        h, w = img_unit.shape[:2]
        # h is 1024. crop center 1024x1024.
        cx = w // 2
        size = h
        x_start = cx - size // 2
        x_end = x_start + size
        img_icon = img_unit[:, x_start:x_end]
        img_icon_resized = cv2.resize(img_icon, (TARGET_ICON_SIZE, TARGET_ICON_SIZE), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite("public/assets/earth_icon.png", img_icon_resized)
        print(f"Saved earth_icon.png: {TARGET_ICON_SIZE}x{TARGET_ICON_SIZE}")

normalize_assets_final()
