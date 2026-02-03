
import cv2
import numpy as np

def despill_magenta():
    src = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    out = "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/earth_minion.png"
    
    print(f"Despilling Magenta Halo from {src}...")
    
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Source not found")
        return
    
    # Identify Magenta-ish pixels
    # Condition: G is the weak channel
    # R > G and B > G
    # And allow some tolerance?
    b, g, r, a = cv2.split(img)
    
    # Mask of pixels to fix
    # We only care about visible pixels (a > 0)
    # Strength of Magenta: (R-G) + (B-G)
    # If Strength > Threshold, Despill.
    # We want to catch the faint pink halo too.
    
    mask = (r > g) & (b > g) & (a > 0)
    
    # Improvement: Only target pixels where R and B are somewhat close?
    # Magenta is R~B.
    # Shadows might be R>G, B>G but R!=B.
    
    # For detected pixels, replace color with Gray (Average of R,B or just G?)
    # Usually standard despill sets G = (R+B)/2... wait, that makes it MORE bright?
    # Green Screen Despill: G -> min(G, B).
    # Magenta Screen Despill: G stays same. Reduce R and B?
    # Set R = G? Set B = G?
    # This turns (255, 0, 255) -> (0, 0, 0).
    # This turns (150, 100, 150) -> (100, 100, 100).
    # This preserves luminance roughly?
    
    # Let's verify:
    # Pink Edge (200, 100, 200).
    # New: (100, 100, 100). Dark Gray. Good for blending into dark background.
    
    # Apply to mask
    img[mask, 0] = img[mask, 1] # B = G
    img[mask, 2] = img[mask, 1] # R = G
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (Despill)")

despill_magenta()
