from PIL import Image, ImageDraw
import numpy as np

def clean_final_version(input_path, output_path):
    # Open as RGBA
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # 1. REMOVE DIAMOND (SPARKLE) IN BOTTOM RIGHT
    # AI watermarks/sparkles are usually in the bottom 5-10% of the image
    # Let's clear a 60x60 area in the bottom right to be safe
    data = np.array(img)
    # Clear bottom right corner
    data[height-60:height, width-60:width, 3] = 0
    
    # 2. BETTER CHECKERBOARD REMOVAL
    # Checkers in Gemini generations are usually:
    # C1: (0,0,0) or (2,2,2) etc.
    # C2: (102,102,102) or similar mid-gray
    
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    
    # Create mask for potential background
    # Very dark checkers
    mask_dark = (r < 45) & (g < 45) & (b < 45)
    # Mid-gray checkers (wider range to be sure)
    mask_gray = (r > 60) & (r < 160) & (g > 60) & (g < 160) & (b > 60) & (b < 160)
    
    # Combine
    checker_mask = (mask_dark | mask_gray).astype(np.uint8) * 255
    
    # Restrict to connected components from edges to avoid internal hair/armor
    from scipy.ndimage import label, binary_dilation
    
    # Dilation helps connect the diagonal checkerboard squares
    dilated = binary_dilation(checker_mask > 0, structure=np.ones((3,3)))
    labeled, num_features = label(dilated)
    
    # Find labels touching edges
    boundary_labels = set()
    boundary_labels.update(labeled[0, :])
    boundary_labels.update(labeled[-1, :])
    boundary_labels.update(labeled[:, 0])
    boundary_labels.update(labeled[:, -1])
    
    if 0 in boundary_labels:
        boundary_labels.remove(0)
        
    bg_mask = np.isin(labeled, list(boundary_labels))
    
    # Explicitly clear the alpha where bg_mask is true
    data[bg_mask, 3] = 0
    
    # 3. EXTRA CLEANUP FOR NEAR-TRANSPARENT NOISE
    # Sometimes there's semi-transparent junk at the edges
    # Any pixel that survived but is very similar to the sample colors 
    # and is near the edge should be removed.
    
    new_img = Image.fromarray(data)
    new_img.save(output_path)
    print(f"Final surgical clean of {input_path} -> {output_path} complete.")

if __name__ == "__main__":
    clean_final_version("public/assets/gemini_unit.png", "public/assets/gemini_unit_clean.png")
