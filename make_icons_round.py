import cv2
import numpy as np
import os

def process_icon(input_name, output_name):
    base_dir = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/"
    input_path = os.path.join(base_dir, input_name)
    output_path = os.path.join(base_dir, output_name)
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Not found {input_name}")
        return

    # Resize to 128x128 (Force Square to fix 'oval' look)
    # Use INTER_AREA for downscaling (Water), INTER_LINEAR or CUBIC for upscaling.
    target_size = 128
    
    # Check if image has alpha
    if img.shape[2] == 3:
        # Add alpha
        b,g,r = cv2.split(img)
        alpha = np.ones_like(b) * 255
        img = cv2.merge([b,g,r,alpha])
        
    resized = cv2.resize(img, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)
    
    # Create Circle Mask
    mask = np.zeros((target_size, target_size), dtype=np.uint8)
    cv2.circle(mask, (target_size//2, target_size//2), target_size//2, 255, -1)
    
    # Apply Mask (Put into Alpha channel)
    # But wait, if original had transparency (e.g. flame shape), applying circle mask essentially crops it to circle.
    # If we want to "Force Round", we assume the content SHOULD fill the circle.
    # But 'element_fire_v4' is a flame shape. If we resize to square, it becomes a fat flame. Masking to circle cuts off corners.
    # User said "want all of them to looks exatcly the same and same sixe shape etc". "want it to be round".
    # Just forcing resizing to square usually makes it "Round-ish" if the original was an orb.
    
    # Let's Try: Resize to Square. keep alpha.
    # If user complained about "Oval", resizing to Square fixes the Aspect Ratio.
    # So I will just Resize to 128x128.
    # The mask ensures it strictly fits in a circle (clips corners).
    
    # Combine existing alpha with circle mask
    b,g,r,a = cv2.split(resized)
    final_a = cv2.bitwise_and(a, mask)
    final_img = cv2.merge([b,g,r,final_a])
    
    cv2.imwrite(output_path, final_img)
    print(f"Saved {output_name}")

process_icon("element_fire_v4.png", "element_fire_circle.png")
process_icon("element_water.png", "element_water_circle.png")
process_icon("element_electric.png", "element_electric_circle.png")
