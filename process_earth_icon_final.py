
import cv2
import numpy as np

def process_earth_icon_borderless():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_element_icon_no_ring_raw_1769882058727.png"
    out_base = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth.png"
    out_circle = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth_circle.png"
    
    print(f"Processing borderless Earth icon from {src}...")
    img = cv2.imread(src)
    if img is None:
        print("Source image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # Locate the central content
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    
    # Use hough circles to find the main circle
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, h/2, param1=50, param2=30, minRadius=int(h*0.3), maxRadius=int(h*0.5))
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        ix, iy, ir = circles[0,0]
        
        # We want to remove the ring. The ring is usually at the edge of the circle.
        # So we crop slightly inside the detected circle to remove the ring.
        inner_r = int(ir * 0.94) # Shave off 6% of the radius to remove any border
        
        # Create mask
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (ix, iy), inner_r, 255, -1)
        
        # Apply mask
        img[:, :, 3] = mask
        
        # Crop to the circle
        side = inner_r * 2
        x1 = max(0, ix - inner_r)
        y1 = max(0, iy - inner_r)
        cropped = img[y1:y1+side, x1:x1+side]
        
        # Standardize to 128x128
        final_icon = cv2.resize(cropped, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        
        cv2.imwrite(out_base, final_icon)
        cv2.imwrite(out_circle, final_icon)
        print(f"Successfully saved borderless Earth icon to {out_base}")
    else:
        print("Could not detect circle automatically.")

process_earth_icon_borderless()
