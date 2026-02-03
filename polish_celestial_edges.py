
import cv2
import numpy as np

def decontaminate_edges(input_path, output_path):
    print(f"Decontaminating green edges: {input_path}")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found.")
        return

    # Split channels
    if img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
    else:
        print("Error: Image has no alpha channel.")
        return

    # De-spill algorithm:
    # If Green is the dominant channel, clamp it to the max of Red and Blue.
    # This removes the green tint from anti-aliased edges.
    
    # Calculate limits
    # We only want to affect pixels where Green is dominant (Green fringe)
    # We can be slightly aggressive since the unit (White/Gold/Blue) shouldn't be Green dominant except the gem.
    # The gem might be affected? The gem is emerald.
    # We should mask this to only apply near transparent edges? 
    # Or just apply globally and see? If the gem turns grey, user might complain.
    # But usually spill suppression is fine.
    
    # Let's try to limit it to pixels where alpha is < 255? 
    # But often the fringe is fully opaque in the alpha channel but colored green.
    
    # Let's use a soft clamp.
    # New Green = min(Green, max(Red, Blue) * 1.1)
    # This reduces green intensity to match others.
    
    max_rb = np.maximum(r, b)
    new_g = np.minimum(g, max_rb).astype(np.uint8)
    
    # We need to mix the new green. 
    # Only apply where Green > max_rb (i.e. Green dominant pixels)
    
    # Wait, the gem IS green dominant. This will kill the gem color.
    # WE MUST NOT kill the gem.
    
    # Strategy 2: Erode Alpha.
    # The green halo is usually on the "outside" of the intended pixels.
    # If we erode alpha slightly, we trim the halo.
    
    kernel = np.ones((2,2), np.uint8) # Small kernel
    a_eroded = cv2.erode(a, kernel, iterations=1)
    
    # However, erosion effectively shrinks the image.
    # Let's combine strategies.
    
    # Improved Strategy:
    # 1. Detect green background pixels (the fringe).
    # 2. Turn them transparent.
    
    # How to detect "Green Fringe"?
    # It resembles the background color `(0, 255, 0)` but darker/mixed.
    # High Green, Low Red/Blue.
    
    # Let's define a mask for "Greenish".
    # G > 100, R < 100, B < 100.
    
    mask_greenish = (g > 100) & (r < 100) & (b < 100)
    
    # But this includes the gem?
    # A gem usually has reflections (White) or darks.
    # A "Green Screen" fringe is usually pure hue 120.
    
    # Let's try aggressive Alpha Edge Cleaning (Matting).
    # Since we have a decent alpha already, let's just tighten it.
    
    img[:, :, 3] = a_eroded # Apply erosion first.
    
    # Save
    cv2.imwrite(output_path, img)
    print(f"Saved to {output_path}")

# Run on current file
path = "public/assets/celestial_valkyrie.png"
decontaminate_edges(path, path)
