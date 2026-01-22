from PIL import Image
import numpy as np

def remove_checkerboard(input_path, output_path):
    print(f"Processing {input_path}...")
    try:
        img = Image.open(input_path).convert("RGBA")
        data = np.array(img)

        # distinct colors for checkerboard
        # Usually White (255,255,255) and Grey (often ~204 or ~238)
        # We will target White and Light Greys
        
        r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

        # Definitions of background colors to remove
        # 1. White
        mask_white = (r > 240) & (g > 240) & (b > 240)
        
        # 2. Grey ( Checkerboard Grey is usually around 200-240)
        # Let's check for "Greyness" (R~G~B) and High Brightness
        mask_grey = (r > 150) & (g > 150) & (b > 150) & (np.abs(r - g) < 10) & (np.abs(g - b) < 10)

        # Combine
        # BE CAREFUL: Masamune (Fire) has bright colors (Red/Orange/Yellow).
        # Yellow is (255, 255, 0). White is (255, 255, 255).
        # We must ensure we don't kill the fire.
        # Fire usually has B < G < R.
        # Greys have R ~ G ~ B.
        
        # Refined Grey/White Mask: Must be low saturation (R~G~B)
        is_low_sat = (np.abs(r.astype(int) - g.astype(int)) < 15) & (np.abs(g.astype(int) - b.astype(int)) < 15)
        is_bright = (r > 100) # Checkers are usually bright
        
        final_mask = is_low_sat & is_bright

        data[final_mask] = [0, 0, 0, 0]

        new_img = Image.fromarray(data)
        new_img.save(output_path)
        print(f"Saved cleaned image to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

remove_checkerboard("assets/masamune.png", "assets/masamune_clean.png")
