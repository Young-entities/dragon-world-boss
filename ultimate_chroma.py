import cv2
import numpy as np

def ultimate_chroma_key(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Image not found")
        return

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Standard Neon Green Range
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    
    bg_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert to get Foreground
    fg_mask = cv2.bitwise_not(bg_mask)
    
    # Erode the Foreground mask significantly (2 iterations) to remove halo
    kernel = np.ones((3,3), np.uint8)
    fg_mask_eroded = cv2.erode(fg_mask, kernel, iterations=2)
    
    # Smooth the mask
    fg_mask_eroded = cv2.GaussianBlur(fg_mask_eroded, (3, 3), 0)
    
    # DESPILL (Color Correction)
    # Reduce Green spill in the remaining pixels
    # Simple algorithm: G = min(G, (R+B)/2)
    # But PROTECT GOLD (where R is high and G is high)
    # Gold: R~255, G~215. R > G.
    # Green Screen: G > R.
    
    b, g, r = cv2.split(img)
    
    # Create mask where Green is dominant (Spill candidate)
    # Condition: G > R and G > B
    spill_mask = (g > r) & (g > b)
    
    # Apply despill only there
    # avg = (r + b) // 2
    # g[spill_mask] = avg[spill_mask] # Can't simple assign, need proper indexing
    
    # Vectorized Despill
    avg_rb = (r.astype(np.int16) + b.astype(np.int16)) // 2
    
    # Only replace G if G > avg_rb inside spill_mask?
    # Actually, standard despill replaces G with avg_rb globally where G > avg_rb?
    # No, that kills Gold.
    # Logic: If G > R (Gold has R > G, so Gold is safe-ish).
    # But light yellow might have G ~ R.
    
    # Let's apply a "Soft Despill": Reduce Green where it is the dominant channel.
    np.putmask(g, spill_mask, avg_rb.astype(np.uint8))
    
    # Re-merge
    img_despilled = cv2.merge([b, g, r])
    b2, g2, r2 = cv2.split(img_despilled)
    
    # Add Alpha from Eroded Mask
    rgba = cv2.merge([b2, g2, r2, fg_mask_eroded])
    
    cv2.imwrite(output_path, rgba)
    print(f"Ultimate Chroma Key (Despilled): {output_path}")

ultimate_chroma_key("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_azaerth_greenscreen_regen_1769702009898.png", "public/assets/dark_deity_unit.png")
