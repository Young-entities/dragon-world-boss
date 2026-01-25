import cv2
import numpy as np

def surgical_master_grade_fix(input_path, output_path):
    # Load EXACT generated image (800x1312)
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. CORE PROTECTION SHIELD (Spatially protect the face and skin)
    # The face center is approx (654, 252) on the 1312x800 image
    fx, fy = 654, 252
    shield = np.zeros((h, w), dtype=np.uint8)
    # Protection zone for face, eyes, and skin (solid 255)
    cv2.circle(shield, (fx, fy + 20), 110, 255, -1) # Face/Neck
    cv2.rectangle(shield, (550, 350), (760, 550), 255, -1) # Body skin area
    
    # 2. TARGET ALL WHITE (Background + Internal Holes)
    # We target anything that is near-white [245, 245, 245] to [255, 255, 255]
    # This catches the "islands" between the dragon heads.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    # Pure white background: Low Saturation (< 25) and High Value (> 235)
    bg_mask = (s < 25) & (v > 235)
    
    # 3. Apply Transparency
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Dissolve if it's Background AND NOT in the Sacred Face Shield
    alpha[bg_mask & (shield == 0)] = 0
    # Hard lock shield area to solid
    alpha[shield == 255] = 255
    
    # 4. CINEMATIC BOTTOM FADE
    # Softly fade the bottom 30 pixels of the sprite so it blends with the ground
    fade_start = 740 # Image ends at 800
    for y in range(fade_start, h):
        factor = 1.0 - (y - fade_start) / (h - fade_start)
        alpha[y, :] = (alpha[y, :] * factor).astype(np.uint8)

    # 5. ASSET POLISH
    rgba[:,:,3] = alpha
    # Remove the 1,800 watermark tag from the bottom right
    # (The fade might already handle it, but let's be sure)
    rgba[750:, 1150:, 3] = 0
    
    # Crop to center the unit better
    rgba = rgba[30:h-10, 100:w-100]
    
    cv2.imwrite(output_path, rgba)
    print(f"Master Grade Fix complete: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
surgical_master_grade_fix(source, "public/assets/water_deity_unit_final.png")
