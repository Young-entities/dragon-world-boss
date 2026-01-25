import cv2
import numpy as np

def fix_face_opacity(input_path, original_path, output_path):
    # Load the transparent version
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    # Load the original white-background version (which has the correct face)
    orig = cv2.imread(original_path)
    if orig is None: return
    
    h, w = img.shape[:2]
    
    # Define a precise shield for the face area
    # y: 150-380, x: 450-530 (based on 1024x1024 or similar)
    # Let's detect the face area or use percentage
    fy1, fy2 = int(h * 0.15), int(h * 0.45)
    fx1, fx2 = int(w * 0.40), int(w * 0.58)
    
    # Restore colors and alpha for the face
    # We copy the colors from the original and set alpha to 255
    # but only for pixels that aren't pure white (the background)
    face_roi_orig = orig[fy1:fy2, fx1:fx2]
    face_roi_img = img[fy1:fy2, fx1:fx2]
    
    # If the original pixel is not white background, make it opaque
    # (Thresholding original white)
    white_thresh = 245
    is_not_white = (face_roi_orig[:,:,0] < white_thresh) | (face_roi_orig[:,:,1] < white_thresh) | (face_roi_orig[:,:,2] < white_thresh)
    
    # Apply
    face_roi_img[is_not_white, :3] = face_roi_orig[is_not_white]
    face_roi_img[is_not_white, 3] = 255
    
    # Save to a final definitive version
    cv2.imwrite(output_path, img)
    print(f"Face transparency fixed. Highlights restored: {output_path}")

fix_face_opacity("public/assets/overlord_perfect_v2.png", "public/assets/overlord_white_bg.png", "public/assets/overlord_absolute_final.png")
