
import cv2
import numpy as np

def finalize_recreated_earth_icon():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_element_recreate_no_ring_raw_1769882106937.png"
    out_base = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth.png"
    out_circle = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/element_earth_circle.png"
    
    print(f"Finalizing recreated Earth icon from {src}...")
    img = cv2.imread(src)
    if img is None:
        print("Source image not found.")
        return

    # Convert to BGRA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # 1. White background removal
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
    # 2. Precise circle detection for cropping
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, h/2, param1=50, param2=30, minRadius=int(h*0.35), maxRadius=int(h*0.5))
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        ix, iy, ir = circles[0,0]
        
        # User wants NO ring. The generated image has a small inner indentation.
        # We'll crop slightly further in to remove that indentation and leave just the wood.
        inner_r = int(ir * 0.88) 
        
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (ix, iy), inner_r, 255, -1)
        
        # Create transparent result
        transparent = np.zeros((h, w, 4), dtype=np.uint8)
        transparent[mask > 0] = img[mask > 0]
        transparent[:, :, 3] = mask
        
        # Crop
        side = inner_r * 2
        x1, y1 = ix - inner_r, iy - inner_r
        final_cropped = transparent[y1:y1+side, x1:x1+side]
        
        # Standardize to 128x128
        final_icon = cv2.resize(final_cropped, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        
        cv2.imwrite(out_base, final_icon)
        cv2.imwrite(out_circle, final_icon)
        print(f"Successfully saved finalized leaf icon to {out_base}")
    else:
        print("Could not detect circle.")

if __name__ == "__main__":
    finalize_recreated_earth_icon()
