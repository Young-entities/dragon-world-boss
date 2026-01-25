import cv2
import numpy as np

def surgical_v2_fix(input_path, output_path):
    # Load the original image with full spear and checkers
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image")
        return

    # 1. Mouth Removal (Surgical Patch)
    # The mouth in the original image is roughly at a different coordinate 
    # since it's a different scale. Let's find it.
    # Estimated for the 1024-scale crop:
    mouth_y, mouth_x = 228, 497 # approximate center of mouth in the user's upload
    
    # Get skin color 
    skin_roi = img[mouth_y-8:mouth_y-5, mouth_x-5:mouth_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8)
    
    # Apply the patch 
    cv2.rectangle(img, (mouth_x - 10, mouth_y - 3), (mouth_x + 10, mouth_y + 3), skin_color.tolist(), -1)
    
    # Blur the patch
    patch_roi = img[mouth_y-8:mouth_y+8, mouth_x-15:mouth_x+15]
    patch_roi = cv2.GaussianBlur(patch_roi, (5,5), 0)
    img[mouth_y-8:mouth_y+8, mouth_x-15:mouth_x+15] = patch_roi

    # 2. Fake Checkered Background Removal
    # We turn to HSV to isolate the character's blue/black/dark tones
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create mask for the "White/Grey" checkers
    # Basically anything that is very low saturation and high value is background
    lower_bg = np.array([0, 0, 200])   # Low saturation, high brightness
    upper_bg = np.array([180, 40, 255]) 
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # Invert to get the character
    char_mask = cv2.bitwise_not(bg_mask)
    
    # Clean up the mask (remove speckles)
    kernel = np.ones((3,3), np.uint8)
    char_mask = cv2.morphologyEx(char_mask, cv2.MORPH_OPEN, kernel)
    char_mask = cv2.GaussianBlur(char_mask, (3,3), 0)

    # Merge to BGRA
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, char_mask])
    
    # Save the result
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V2 Fix completed: {output_path}")

# Run on the original uploaded image
surgical_v2_fix("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769301101122.png", "public/assets/water_deity_fixed_v2.png")
