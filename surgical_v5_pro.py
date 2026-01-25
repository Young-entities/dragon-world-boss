import cv2
import numpy as np

def surgical_v5_pro(input_path, output_path):
    # Load the original high-res image with white background
    # (The one that has the full spear and no mouth)
    img = cv2.imread(input_path)
    if img is None: return
    
    h, w = img.shape[:2]

    # 1. Protection Mask (The "Sacred Zone")
    # We create a mask for the core character area where we NEVER want transparency.
    # This covers the face, chest, and core body highlights.
    protection_mask = np.zeros((h, w), dtype=np.uint8)
    
    # Face & Body Core: Protect from roughly (400, 150) to (620, 500)
    # Coordinate estimate for the character in the 1024x1024 frames:
    # Top-center head: x=512, y=250
    cv2.rectangle(protection_mask, (440, 200), (580, 500), 255, -1)
    
    # Also protect some of the dragons' central parts if needed, but let's start with the lady
    
    # 2. Transparency Logic
    # Convert image to grayscale for background detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold: anything brighter than 250 is usually background
    _, alpha = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY_INV)
    
    # 3. Apply Protection
    # Rule: If it's in the protection mask, it MUST be 255 (opaque)
    alpha = cv2.bitwise_or(alpha, protection_mask)
    
    # 4. Refinement
    # Remove tiny speckles in the background
    kernel = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
    
    # Smooth edges for natural blending
    alpha = cv2.GaussianBlur(alpha, (5,5), 0)
    
    # 5. Restore Color Consistency
    # Split the original BGR and merge with our new smart alpha
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    cv2.imwrite(output_path, rgba)
    print(f"Surgical V5 PRO (Protection Layer) completed: {output_path}")

# Using the nosed version as base
surgical_v5_pro("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_deity_nosed_white_bg_1769301126078.png", "public/assets/water_deity_unit_final.png")
