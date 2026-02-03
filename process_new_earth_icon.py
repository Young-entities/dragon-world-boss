
import cv2
import numpy as np

def process_new_earth_icon():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_element_icon_new_raw_1769881160335.png"
    out_base = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth.png"
    out_circle = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth_circle.png"
    
    print(f"Processing new Earth icon from {src}...")
    img = cv2.imread(src)
    if img is None:
        print("Source image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # Remove white background
    # Use floodfill starting from corners
    mask = np.zeros((h+2, w+2), np.uint8)
    # Floodfill top-left corner white if it is white
    if np.all(img[0,0,:3] > 240):
        cv2.floodFill(img, mask, (0,0), (0,0,0,0), (5,5,5), (5,5,5), flags=4 | cv2.FLOODFILL_FIXED_RANGE)
    
    # Locate the central content to find the circle
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, h/2, param1=50, param2=30, minRadius=int(h*0.3), maxRadius=int(h*0.5))
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        ix, iy, ir = circles[0,0]
        
        # We want to replace the gray metallic frame with a black border.
        # The metallic frame is roughly between 0.85*ir and 1.0*ir
        
        # Create a new image with a black border
        # Clear out everything outside inner content radius (approx 0.83 * ir)
        inner_r = int(ir * 0.83)
        
        final_img = np.zeros((h, w, 4), dtype=np.uint8)
        
        # Core mask (the leaf/rock part)
        core_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(core_mask, (ix, iy), inner_r, 255, -1)
        
        # Copy core content
        final_img[core_mask > 0] = img[core_mask > 0]
        
        # Draw a solid black border
        # Border thickness approx 6-8 pixels
        thickness = 8
        cv2.circle(final_img, (ix, iy), inner_r + thickness//2, (0,0,0,255), thickness)
        
        # Crop to the circle
        side = (inner_r + thickness + 10) * 2
        x1 = max(0, ix - side//2)
        y1 = max(0, iy - side//2)
        cropped = final_img[y1:y1+side, x1:x1+side]
        
        # Resize to standard 128x128 for icons
        final_icon = cv2.resize(cropped, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        
        cv2.imwrite(out_base, final_icon)
        cv2.imwrite(out_circle, final_icon)
        print(f"Saved new Earth icon with black border to {out_base}")
    else:
        # Fallback if circle detection fails: just remove white and save
        # Actually let's try a different approach if circle detection fails
        print("Circle detection failed, using alternative masking...")
        # Get bounding box of non-transparent
        alpha = img[:,:,3]
        coords = cv2.findNonZero(alpha)
        if coords is not None:
            x,y,w,h = cv2.boundingRect(coords)
            # Find center
            cx, cy = x + w//2, y + h//2
            r = min(w, h) // 2
            
            # Draw black circle
            cv2.circle(img, (cx, cy), r-4, (0,0,0,255), 10)
            # Crop to circle
            res = img[cy-r:cy+r, cx-r:cx+r]
            res = cv2.resize(res, (128, 128), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(out_base, res)
            cv2.imwrite(out_circle, res)

process_new_earth_icon()
