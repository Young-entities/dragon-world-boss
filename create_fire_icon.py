import cv2
import numpy as np

def create_fire_icon():
    # Use the PROCESSED Unit Image (Transparent)
    unit_path = "public/assets/fire_empress_unit.png"
    output_path = "public/assets/fire_empress_icon.png"
    
    img = cv2.imread(unit_path)
    if img is None:
        print("Unit load failed")
        return

    # Algorithm to find Face and Crop
    # The image is Green Screen.
    # We can detect the non-green pixels.
    # The Face is likely in the Top Center of the bounding box.
    
    # Template Matching to find Face
    template_path = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769715576543.png"
    template = cv2.imread(template_path)
    if template is None:
        print("Template not found, using fixed crop")
        # Fallback to fixed
        center_x = 450
        center_y = 250
    else:
        # Match
        # Resize template? It might be small/different scale.
        # But Pattern Matching is robust?
        # Let's try matching. 
        # Convert both to gray? Not necessary but faster.
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        # Max Loc is top-left of match.
        h_t, w_t = template.shape[:2]
        center_x = max_loc[0] + w_t // 2
        center_y = max_loc[1] + h_t // 2
        print(f"Face found at {center_x}, {center_y} with score {max_val}")

    # Tight Crop for Close Up (Like Zylos)
    icon_size = 60 # ULTRA Extreme face crop
    
    x1 = max(0, center_x - icon_size // 2)
    y1 = max(0, center_y - icon_size // 2)
    x2 = min(img.shape[1], x1 + icon_size)
    y2 = min(img.shape[0], y1 + icon_size)
    
    crop = img[y1:y2, x1:x2]
    
    # 4. Remove Green BG in Crop (optional, icons usually square with background visible? 
    # Or transparency? Most game icons have a background.
    # The reference icon user uploaded had a background (from the unit art).
    # Since Source is Green Screen, the Icon will have Green Background.
    # We should REPLACE Green with something else? Or Transparent?
    # User uploaded a crop WITH NO GREEN (it was close up on face with hair filling frame).
    # I'll just save it. If green shows, I'll fix.
    # Actually, Pyra has BIG HAIR. It likely fills the icon.
    
    # Resize to 100x100
    final = cv2.resize(crop, (100, 100), interpolation=cv2.INTER_AREA)
    
    cv2.imwrite(output_path, final)
    print(f"Icon Created: {output_path}")

create_fire_icon()
