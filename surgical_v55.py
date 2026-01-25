import cv2
import numpy as np

def surgical_v55_puddle_fix(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    h, w = img.shape[:2]

    # Convert to BGRA if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Target the bottom 30% of the image where the puddle is
    puddle_start_y = int(h * 0.70)
    
    # ROI (Region of Interest)
    roi = img[puddle_start_y:h, 0:w]
    
    # Create a mask for white/light-greyish background pixels in the puddle area
    # Adjust thresholds to catch the background but preserve the blue water
    # Water is blue, so Blue channel will be high, bit Red/Green will be lower.
    # White background has high R, G, and B.
    
    # Define range for white/light-grey background
    # We want to remove pixels that are high in all 3 channels (bright)
    # But we must preserve the light blue parts of the water.
    # Light blue water: High B, Medium G, Low-Medium R.
    # White background: High B, High G, High R.
    
    # Aggressive Strategy: Channel Balance
    # Background pixels are neutral (R~=G~=B). Blue water is NOT (B >> R, B >> G).
    b = roi[:,:,0]
    g = roi[:,:,1]
    r = roi[:,:,2]
    
    # Condition 1: Brightness. Must be relatively bright.
    bright_mask = (b > 160) & (g > 160) & (r > 160)
    
    # Condition 2: Neutrality. |R-G| < 20, |G-B| < 20, |B-R| < 20
    # However, water is BLUE. So for water, B is usually 30+ higher than R or G.
    # So we want to kill anything where B is NOT significantly higher than R/G.
    
    # If B is close to G (within 30), it's probably grey/white/cyan background, not deep blue water.
    diff_bg = np.abs(b.astype(int) - g.astype(int)) < 30
    diff_br = np.abs(b.astype(int) - r.astype(int)) < 30
    
    # Combined: Bright AND Neutral(ish)
    puddle_mask = bright_mask & diff_bg & diff_br
    
    # Apply removal
    roi[puddle_mask, 3] = 0
    
    # Apply back to image
    img[puddle_start_y:h, 0:w] = roi
    
    # Also, to address "cropped out" look at the very bottom edge, 
    # lets add a slight transparency gradient fade to the very last 5-10 pixels 
    # so the hard line isn't as visible.
    fade_height = 10
    if h > fade_height:
        for i in range(fade_height):
            y = h - fade_height + i
            alpha_factor = 1.0 - (i / float(fade_height)) # 1.0 down to 0.0
            # Multiply existing alpha by factor
            current_alpha = img[y, :, 3]
            new_alpha = (current_alpha * alpha_factor).astype(np.uint8)
            img[y, :, 3] = new_alpha

    cv2.imwrite(output_path, img)
    print(f"Puddle Fixed: {output_path}")

source = "public/assets/water_deity_unit_final.png"
surgical_v55_puddle_fix(source, "public/assets/water_deity_unit_final.png")
