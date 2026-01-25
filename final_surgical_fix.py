from PIL import Image
import numpy as np

def final_surgical_fix(input_path, output_path):
    # Load original unit
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    h, w = r.shape

    # 1. HARD ERASE DIAMOND (Bottom Right)
    # Wiping 100x100 to be absolutely sure
    a[h-100:, w-100:] = 0

    # 2. CHECKERBOARD TARGETING
    # The grid colors are mathematically neutral (R=G=B)
    # The character's face and sword have WARM tones (R > G > B)
    
    # Threshold for "Neutrality"
    # If the difference between R, G, and B is less than 5, it's a checker
    diff_rg = np.abs(r.astype(int) - g.astype(int))
    diff_gb = np.abs(g.astype(int) - b.astype(int))
    is_neutral = (diff_rg < 6) & (diff_gb < 6)
    
    # Targeted colors: 
    # Black: < 50
    # Gray: 90 to 120
    is_checker_color = ((r < 55) | ((r > 80) & (r < 135)))
    
    bg_mask = is_neutral & is_checker_color
    
    # 3. PROTECTION FOR FACE AND CHARACTER
    # Character skin/face/vibrant armor is NEVER perfectly neutral.
    # We will only delete neutral pixels that are NOT vibrant.
    # Vibrant = (Max - Min) > 10
    vibrancy = np.max(data[:,:,:3], axis=2).astype(int) - np.min(data[:,:,:3], axis=2).astype(int)
    is_vibrant = vibrancy > 12
    
    # Final clear: Is Neutral AND is Checker Color AND is NOT Vibrant
    to_delete = bg_mask & (~is_vibrant)
    
    a[to_delete] = 0
    
    # 4. EDGE POLISH
    # Sometimes a thin gray line remains at the borders.
    # We'll clear the outermost 5 pixels entirely.
    a[0:5, :] = 0
    a[-5:, :] = 0
    a[:, 0:5] = 0
    a[:, -5:] = 0

    # Save as a brand NEW filename to force browser reload
    new_img = Image.fromarray(data)
    new_img.save(output_path)
    print(f"Definitive fix saved to {output_path}")

# Run on the ORIGINAL asset
final_surgical_fix("public/assets/gemini_unit.png", "public/assets/gemini_unit_transparent.png")
