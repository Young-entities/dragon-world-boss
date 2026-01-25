import cv2
import numpy as np

def crop_inner_icon(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
    
    h, w = img.shape[:2]
    
    # Define the crop area to remove the frame
    # Based on the image, the frame is quite thick. 
    # Let's take the inner ~75% to get a good close-up without any border.
    
    # Calculate margins (roughly 12.5% on each side to remove the frame)
    margin_y = int(h * 0.12)
    margin_x = int(w * 0.12)
    
    # Crop it
    cropped = img[margin_y:h-margin_y, margin_x:w-margin_x]
    
    # One more check for the watermark (if it survived the crop)
    # The watermark is in the extreme bottom-right of the ORIGINAL.
    # It might be gone now, but let's be sure the bottom right of the CROP is clean.
    ch, cw = cropped.shape[:2]
    artifact_roi = cropped[ch-50:, cw-50:]
    avg_col = np.median(cropped[ch-100:ch-50, cw-100:cw-50].reshape(-1, 3), axis=0)
    
    # Simple check for bright pixels in the corner
    gray = cv2.cvtColor(artifact_roi, cv2.COLOR_BGR2GRAY)
    if np.max(gray) > 200:
        cropped[ch-40:, cw-40:] = avg_col
        print("Secondary watermark cleanup on crop performed.")

    cv2.imwrite(output_path, cropped)
    print(f"Cropped close-up icon saved (no frame): {output_path}")

# Run on the original high-quality face card
crop_inner_icon("c:/Users/kevin/New folder (2)/Gemini_Generated_Image_otvau1otvau1otva.png", "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/overlord_icon_no_frame.png")
