import cv2
import numpy as np

def cinematic_blend_fix(input_path, output_path):
    # Load the processed sprite
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    h, w, c = img.shape
    if c < 4:
        print("Image doesn't have alpha channel. Something is wrong.")
        return

    # 1. SOFT BOTTOM FADE
    # We want to fade the last 15-20 pixels so the straight line disappears
    fade_height = 20
    for y in range(h - fade_height, h):
        # Calculate fade factor (1 at h-fade_height, 0 at h)
        alpha_mult = 1.0 - (y - (h - fade_height)) / fade_height
        img[y, :, 3] = (img[y, :, 3] * alpha_mult).astype(np.uint8)

    # 2. INTERNAL CLEANUP (Optional)
    # Target any remaining microscopic white speckles in the water gaps
    # (High brightness, low saturation)
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    inner_glitch = (hsv[:,:,1] < 30) & (hsv[:,:,2] > 240)
    # Only remove if they aren't protected core
    # (Leaving this skipped for now to avoid the 'hollow face' issue again)

    # 3. Final Frame Polish
    # Crop 1 pixel off each side to kill any single-pixel edge lines
    img = img[1:h-1, 1:w-1]

    cv2.imwrite(output_path, img)
    print(f"Cinematic Blend complete: {output_path}")

source = "public/assets/water_deity_unit_final.png" # Using the one we just made
cinematic_blend_fix(source, "public/assets/water_deity_unit_final.png")
