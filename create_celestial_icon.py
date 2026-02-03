
import cv2
import numpy as np

def create_icon(input_path, output_path):
    print(f"Creating icon from: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found.")
        return

    # Source is 900x600. Content is 691x588 centered.
    # Content Start Y = 6.
    # Content Center X = 450.
    
    # We want a 200x200 icon of the face/upper body.
    # Let's verify content location?
    # Actually, we know I just centered it.
    
    # Let's target the "Head".
    # Assuming head is near the top of content.
    # Let's crop centered horizontally, and from the top vertically.
    
    # Crop Region:
    # X: 350 to 550 (200px width centered at 450)
    # Y: 20 to 220 (200px height starting near top)
    # Adjusted Y=20 to avoid tip of spear/halo being only thing seen.
    
    # Better: Scan for content top.
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            # Center X of content
            cx = x + w // 2
            
            # Crop 200x200 around CX, Top Y
            # But we might need to zoom in? 
            # A 200px crop might be too small (pixelated) or too zoomed in?
            # 600px height. 200px is 1/3 height. That's a good headshot size.
            
            x1 = cx - 100
            y1 = y + 20
            
            # Ensure bounds
            x1 = max(0, x1)
            y1 = max(0, y1)
            
            crop = img[y1:y1+200, x1:x1+200]
            
            # If crop is smaller than 200x200 (if near edges), pad it?
            if crop.shape[0] < 200 or crop.shape[1] < 200:
                print("Padding crop to 200x200")
                padded = np.zeros((200, 200, 4), dtype=np.uint8)
                padded[:crop.shape[0], :crop.shape[1]] = crop
                crop = padded
            
            cv2.imwrite(output_path, crop)
            print(f"Saved icon to {output_path}")

path = "public/assets/celestial_valkyrie.png"
out = "public/assets/celestial_icon.png"
create_icon(path, out)
