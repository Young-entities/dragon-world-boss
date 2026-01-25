import cv2
import numpy as np

def surgical_deity_fix(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not load image")
        return

    # 1. Mouth Removal (Surgical Patch)
    # The face is roughly at x=450-550, y=200-350 for a 1024x1024 image
    # Let's find the skin tone near the mouth and patch it.
    # Looking at the image, the mouth area is approximately:
    # y: 265-280, x: 495-515
    
    # We will use seamlessClone or just a simple median patch
    mouth_y, mouth_x = 278, 502 # approximate center of mouth
    h, w = 8, 12 # size of patch
    
    # Get skin color from just above the mouth (under the nose)
    skin_roi = img[mouth_y-15:mouth_y-10, mouth_x-5:mouth_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8)
    
    # Apply the patch to remove the mouth line
    # We'll use a blurred circle patch to make it look natural
    cv2.rectangle(img, (mouth_x - 10, mouth_y - 4), (mouth_x + 10, mouth_y + 4), skin_color.tolist(), -1)
    
    # Optional: Slightly blur the patched area
    face_roi = img[mouth_y-10:mouth_y+10, mouth_x-15:mouth_x+15]
    face_roi = cv2.GaussianBlur(face_roi, (5,5), 0)
    img[mouth_y-10:mouth_y+10, mouth_x-15:mouth_x+15] = face_roi

    # 2. Transparency Implementation
    # Convert to BGRA
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Refine alpha: remove small artifacts and smooth edges
    kernel = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
    alpha = cv2.GaussianBlur(alpha, (3,3), 0)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])
    
    # Save the result
    cv2.imwrite(output_path, rgba)
    print(f"Surgical Deity Fix completed: {output_path}")

# Note: The path below might need adjustment based on the actual filename
surgical_deity_fix("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/water_deity_nosed_white_bg_1769301126078.png", "public/assets/water_deity_unit_final.png")
