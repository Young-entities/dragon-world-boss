
import cv2
import numpy as np

def remove_green_objects(input_path, output_path):
    print(f"Removing remaining green objects from: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    # Convert RGB to HSV
    # Note: OpenCV loads BGRA.
    b, g, r, a = cv2.split(img)
    img_bgr = cv2.merge([b, g, r])
    
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    
    # Detect Green Hue
    # Range: 35 - 85
    lower = np.array([30, 40, 40])
    upper = np.array([90, 255, 255])
    
    mask = cv2.inRange(hsv, lower, upper)
    
    # We want to remove these green parts.
    # But wait, what if the spear handle is greenish? 
    # Or the eyes? (User said "no mouth or nose", eyes remain).
    # Eyes are usually blue/gold/green.
    # If eyes are green, this will blind her.
    # User said "look at here floting thing on her head". Specific target.
    # "floating thing on her head" -> Star.
    # If the star has green gems, this removes them.
    # "weapon" -> Spear.
    # If spear has green gems, this removes them.
    # User said "not lall the green got off".
    
    # This implies the green is unwanted background/residue OR unwanted green objects.
    # Given the aggression "why cant u just make her background transparent the green",
    # I assume ALL green is considered "Background/Error".
    
    # Apply mask to Alpha
    # Set Alpha = 0 where mask is Green
    
    # Dilate the mask slightly to catch edges of the green objects
    kernel = np.ones((3,3), np.uint8)
    mask_dilated = cv2.dilate(mask, kernel, iterations=1)
    
    # Only mask where alpha was > 0 (don't expand into empty space, irrelevant)
    
    # Update alpha
    # Use inverted mask: keep pixels that are NOT green
    keep_mask = cv2.bitwise_not(mask_dilated)
    
    new_a = cv2.bitwise_and(a, keep_mask)
    
    img[:, :, 3] = new_a
    
    cv2.imwrite(output_path, img)
    print(f"Saved to {output_path}")

path = "public/assets/celestial_valkyrie.png"
remove_green_objects(path, path)
