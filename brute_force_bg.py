import cv2
import numpy as np

def brute_force_bg_fix(input_path, output_path):
    # Always start from the original source to avoid stacking errors
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]
    
    # Coordinates for the diamond based on previous detection (y=704, x=1126)
    # To be absolutely sure, we'll wipe the entire bottom right corner 150x150
    # but instead of a flat color, we'll "clone" the texture from just above it.
    
    # Source area (a patch of fire above the diamond)
    patch_size = 150
    # The diamond is roughly at the corner. Let's take a patch from a bit higher up.
    src_y1 = h - (patch_size * 2)
    src_y2 = h - patch_size
    src_x1 = w - patch_size
    src_x2 = w
    
    # Destination (where the diamond/artifact is)
    dst_y1 = h - patch_size
    dst_y2 = h
    dst_x1 = w - patch_size
    dst_x2 = w
    
    # Copy patch
    patch = img[src_y1:src_y2, src_x1:src_x2].copy()
    # Mirror it or flip it slightly to avoid obvious repetition
    patch = cv2.flip(patch, 0) 
    
    # Paste and blend
    img[dst_y1:dst_y2, dst_x1:dst_x2] = patch
    
    # Apply a heavy blur to the seam line only to hide the cut
    seam_y = dst_y1
    img[seam_y-10:seam_y+10, dst_x1:dst_x2] = cv2.GaussianBlur(img[seam_y-10:seam_y+10, dst_x1:dst_x2], (15,15), 0)

    # Save to a completely NEW filename
    cv2.imwrite(output_path, img)
    print(f"Brute-force texture patch saved to {output_path}")

brute_force_bg_fix("public/assets/gemini_bg.png", "public/assets/bg_final_no_mercy.png")
