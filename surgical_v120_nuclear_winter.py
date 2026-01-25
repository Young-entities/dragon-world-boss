import cv2
import numpy as np
import glob
import os

def surgical_v120_nuclear_winter(output_path):
    # 1. Source
    search_pattern = "../Gemini_*.png"
    files = glob.glob(search_pattern) + glob.glob("Gemini_*.png")
    if not files: return
    latest_file = max(files, key=os.path.getmtime)
    print(f"Using source: {latest_file}")
    
    img = cv2.imread(latest_file)
    # Convert BGR to BGRA
    b, g, r = cv2.split(img)
    
    # 2. RAW EXTRACTION (Black BG Logic)
    # Brightness < 45 = Background
    brightness = r.astype(int) + g.astype(int) + b.astype(int)
    is_bg = brightness < 45
    alpha = np.ones_like(r, dtype=np.uint8) * 255
    alpha[is_bg] = 0
    
    # 3. BLACK LINE UN-STICKER (From V108)
    # Turn Black/Dark pixels to Deep Blue
    is_dark_line = (brightness < 80)
    # But we will handle this via Nuclear Winter globally now.
    
    # 4. NUCLEAR WINTER (Kill Red Channel)
    # User complains about "Orange Aura". Orange needs Red.
    # If we remove Red from the equation, Orange is impossible.
    
    # Define Safe Zone (Skin) - Center Column
    h, w = img.shape[:2]
    col_x0, col_x1 = int(w*0.43), int(w*0.57) # Narrow center
    col_y0, col_y1 = int(h*0.20), int(h*0.60) # Upper Body
    h_idx, w_idx = np.indices((h, w))
    in_skin_zone = (w_idx >= col_x0) & (w_idx <= col_x1) & (h_idx >= col_y0) & (h_idx <= col_y1)
    
    # Create the "Frozen" version of Red channel
    # Where R=0. But maybe blend it? No, user said "Easy", let's be absolute.
    # Set Red to 0 for everything outside skin.
    # This turns White Ice -> Cyan Ice (G, B).
    # This turns Orange Rust -> Dark Green/Black.
    # This turns Black Outline -> Black Outline.
    
    frozen_r = r.copy()
    frozen_r[~in_skin_zone] = 0
    
    # But wait! The Ice SHOULD contain some white (R,G,B=255).
    # If we kill R, white becomes Cyan.
    # Maybe we only kill Red if Red > Blue? (Warmth)
    # Yes, let's stick to the "Kill Warmth" logic but be aggressive.
    
    # Logic: If Pixel is NOT Skin Zone...
    # New_Red = min(Old_Red, Old_Blue).
    # This ensures Red never exceeds Blue.
    # Thus, Pixel is never "Warm".
    # White (255, 255, 255) -> min(255, 255) = 255. White stays White!
    # Orange (200, 100, 50) -> min(200, 50) = 50. Becomes (50, 100, 50) -> Dark Greenish Blue.
    # Brown (100, 50, 20) -> min(100, 20) = 20. -> Dark Blue.
    
    new_r = r.copy()
    outside_skin = ~in_skin_zone
    
    # Apply the "Cooling Filter": R cannot exceed B.
    # We use numpy minimum to clamp R to B in the outside zone.
    
    current_r = r[outside_skin]
    current_b = b[outside_skin]
    clamped_r = np.minimum(current_r, current_b)
    
    # Update Red Channel
    new_r[outside_skin] = clamped_r
    
    # Also clamp Green? Orange has Green.
    # If G > B, it looks Teal/Green. That's fine for Ice.
    
    # 5. BLACK OUTLINE FIX
    # The black outline is R,G,B ~ 0.
    # We want it to be Blue.
    # Set Blue channel to 80 where Brightness < 60
    new_b = b.copy()
    is_very_dark = (brightness < 60) & outside_skin # Only affect armor/dragons
    new_b[is_very_dark] = 100 # Dark Blue
    
    # 6. SHAVE (2px)
    kernel = np.ones((2,2), np.uint8)
    alpha = cv2.erode(alpha, kernel, iterations=2)
    
    # Artifact Clean
    alpha[0:50, 0:50] = 0
    
    # Save
    final_img = cv2.merge([new_b, g, new_r, alpha])
    final_img[alpha == 0] = 0
    
    cv2.imwrite(output_path, final_img)
    print(f"Surgical V120 Nuclear Winter Complete: {output_path}")

surgical_v120_nuclear_winter("public/assets/water_deity_unit_final.png")
