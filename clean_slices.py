
import cv2
import numpy as np
import os

asset_dir = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets"

def clean_lava(name):
    path = os.path.join(asset_dir, f"btn_{name}_exact.png")
    if not os.path.exists(path):
        return
        
    img = cv2.imread(path)
    if img is None: return
    
    # Add alpha
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img.shape[:2]
    
    # Create a Rounded Rectangle Mask
    # The buttons are roughly rounded rects.
    # We want to keep the center opaque, make corners transparent.
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Radius: The buttons look like they have ~15px radius.
    # We can try to fit a contour? 
    # Or just hardcode a safe trim.
    # The padding was 15px.
    # Let's assume the button touches the edges of the crop minus padding?
    # Actually, the slicing script added padding.
    # So the button is in the center.
    
    # Let's use simple thresholding to find the "Stone Frame" vs "Lava".
    # Stone is grey. Lava is Red/Orange/Black.
    # This is hard.
    
    # Plan B: aggressive corner cutting.
    # Radius 25px?
    
    # Draw a filled rounded rect in the mask
    # Inset by 5 pixels to be safe?
    # Verify the slicing script padding. It was 15.
    # So we should shave off ~10px of "Lava" from the edges?
    # Let's crop the image first to remove the explicit padding I added?
    # Wait, the 15px padding was to ENABLE capturing the frame if the contour was tight.
    
    # Let's just create a mask that is an oval/rounded rect covering 90% of the image.
    radius = 20
    cv2.circle(mask, (radius, radius), radius, (255), -1)
    cv2.circle(mask, (w-radius, radius), radius, (255), -1)
    cv2.circle(mask, (radius, h-radius), radius, (255), -1)
    cv2.circle(mask, (w-radius, h-radius), radius, (255), -1)
    cv2.rectangle(mask, (radius, 0), (w-radius, h), (255), -1)
    cv2.rectangle(mask, (0, radius), (w, h-radius), (255), -1)
    
    # Apply mask
    # However, this assumes the extracted image IS exactly the button size.
    # If the extraction had extra space, this mask might be misaligned.
    
    # Let's Resize the mask to the image?
    # The mask is already h,w.
    
    # Apply
    img[:, :, 3] = mask
    
    # Save
    cv2.imwrite(path, img)
    print(f"cleaned {name}")

clean_lava("blue")
clean_lava("green")
clean_lava("red")
