import cv2
import numpy as np

def make_all_white_transparent(input_path, output_path):
    # Load EXACT generated image (800x1312)
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 1. CORE PROTECTION SHIELD (Spatially protect the face and light armor bits)
    # This prevents the transparency from eating holes in her face.
    # The face center is approx (654, 252) on the 1312x800 image
    fx, fy = 654, 252
    shield = np.zeros((h, w), dtype=np.uint8)
    
    # Shield face/eyes/skin
    cv2.circle(shield, (fx, fy + 20), 100, 255, -1) 
    # Shield some core armor highlights that might be too white
    cv2.rectangle(shield, (580, 400), (730, 520), 255, -1)
    
    # 2. TARGET ALL WHITE PIXELS
    # We look for pixels that are very close to pure white.
    # In AI images, white background is usually [254, 254, 254] or [255, 255, 255]
    lower_white = np.array([245, 245, 245])
    upper_white = np.array([255, 255, 255])
    
    white_mask = cv2.inRange(img, lower_white, upper_white)
    
    # 3. Apply Transparency
    # We turn off the alpha channel for white pixels, but ONLY IF they aren't protected.
    rgba[white_mask == 255, 3] = 0
    rgba[shield == 255, 3] = 255 # Force solid for the face
    
    # 4. Save
    # No resizing, no bottom fade, no nose edits. Pure transparency for white pixels.
    cv2.imwrite(output_path, rgba)
    print(f"Global white transparency applied: {output_path}")

source = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
make_all_white_transparent(source, "public/assets/water_deity_unit_final.png")
