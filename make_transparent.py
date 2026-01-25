import cv2
import numpy as np

def make_white_transparent(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load image from {input_path}")
        return

    # Convert to BGRA
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Define the range for white pixels
    # In a generated image, white might not be exactly 255.
    # We use a threshold.
    lower_white = np.array([240, 240, 240, 255])
    upper_white = np.array([255, 255, 255, 255])

    # Create a mask for white pixels
    white_mask = cv2.inRange(bgra, lower_white, upper_white)

    # Set white pixels' alpha to 0
    bgra[white_mask == 255, 3] = 0

    # Optional: Smooth the alpha edge
    # This can help with anti-aliasing artifacts
    alpha = bgra[:, :, 3]
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    bgra[:, :, 3] = alpha

    # Save the result
    cv2.imwrite(output_path, bgra)
    print(f"Transparency applied and saved to {output_path}")

input_img = r"C:\Users\kevin\New folder (2)\Gemini_Generated_Image_nkxb7lnkxb7lnkxb.png"
output_img = r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets\water_deity_unit_final.png"

make_white_transparent(input_img, output_img)
