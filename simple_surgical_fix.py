import cv2
import numpy as np

def simple_surgical_fix(input_path, output_path):
    # Load original image from root
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
        
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape

    # 1. Target the Checkerboard colors (Neutral/Gray/Black)
    diff = np.max(img[:,:,:3], axis=2).astype(int) - np.min(img[:,:,:3], axis=2).astype(int)
    is_neutral = diff < 12 
    
    # 2. DEFINITIVE PROTECTORS (The "No-Touch" Zones)
    # This acts as a barrier so the face and sword stay 100% original.
    protection_shield = np.zeros_like(a, dtype=bool)
    # y range 100 to 500, x range 400 to 850 covers head/torso/sword
    protection_shield[100:550, 380:880] = True 

    # 3. Apply Alpha Wipe
    # Delete neutral colors that are NOT inside our protected character block
    to_clear = is_neutral & (~protection_shield)
    
    # Also wipe the AI logo in the corner no matter what
    to_clear[h-100:, w-100:] = True
    
    # Wipe the edges too to be safe
    to_clear[0:10, :] = True
    to_clear[-10:, :] = True
    to_clear[:, 0:10] = True
    to_clear[:, -10:] = True
    
    a[to_clear] = 0
    
    # One last refined pass: Flood fill the outer background to catch islands
    # but only on the outside of the shield
    
    # Actually, this is already 100 times safer.
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Fixed original character saved to {output_path}")

# Run on the original image you liked
simple_surgical_fix("c:/Users/kevin/New folder (2)/Gemini_Generated_Image_c4req0c4req0c4re.png", "c:/Users/kevin/New folder (2)/monster-warlord/public/assets/overlord_final.png")
