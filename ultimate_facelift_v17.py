import cv2
import numpy as np

def theatrical_facelift_v17(input_path, output_path):
    # Load the high-quality source with checkers (to ensure no quality loss)
    img = cv2.imread(input_path)
    if img is None: return
    h, w = img.shape[:2]

    # Target Face Center (Original Coords)
    fx, fy = 163, 62
    
    # 1. FACIAL SOLIDIFICATION
    # Sample skin tone from a safe spot (forehead)
    skin_roi = img[fy-12:fy-8, fx-5:fx+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Patch the "Mouth" area (smoothly)
    # We use a small blur over the patch to make it look like natural skin
    mouth_zone = img[fy+8:fy+15, fx-10:fx+10]
    cv2.circle(img, (fx, fy + 11), 2, skin_color, -1)
    
    # 2. THE MASTERPIECE NOSE (3D Shaded)
    # Most anime noses are a 'tick' with a shadow and a tiny highlight.
    # Shadow Color (35% darker than skin)
    shadow_color = (np.array(skin_color) * 0.65).astype(np.uint8).tolist()
    # Highlight Color (Brightest skin tone)
    light_color = (np.array(skin_color) * 1.1).clip(0, 255).astype(np.uint8).tolist()
    
    # Draw the main nose bridge shadow (a sharp vertical line)
    cv2.line(img, (fx, fy + 4), (fx, fy + 7), shadow_color, 1)
    # Draw the small "nose tip" tick
    cv2.line(img, (fx, fy + 7), (fx + 1, fy + 7), shadow_color, 1)
    # Add a tiny 1-pixel highlight right next to it to give it depth
    cv2.rectangle(img, (fx + 1, fy + 5), (fx + 1, fy + 6), light_color, -1)

    # 3. BACKGROUND ERASE (Checkers Only)
    # Target exact checker pattern RGBs: [255,255,255] and [239,239,239]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    
    # Create mask for White and Light Grey
    bg_mask = (s < 45) & (v > 175)
    
    # PROTECTION: We create a "Sacred Shield" around the face/body
    protection = np.zeros((h, w), dtype=np.uint8)
    # Shield face area
    cv2.rectangle(protection, (140, 30), (185, 90), 255, -1)
    # Shield Body area
    cv2.rectangle(protection, (100, 90), (220, 200), 255, -1)
    
    # 4. Final Alpha
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Dissolve if it's Background AND not protected
    alpha[bg_mask & (protection == 0)] = 0
    # Hard force protection (Face/Body MUST stay solid)
    alpha[protection == 255] = 255
    
    # 5. SPRITE CLEANUP
    rgba = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], alpha])
    
    # Remove outer black frame/watermark tag
    rgba = rgba[10:h-12, 12:w-12]
    nh, nw = rgba.shape[:2]
    
    # 6. HD RECONSTRUCTION (4x Lanczos-4)
    final_hd = cv2.resize(rgba, (nw * 4, nh * 4), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final_hd)
    print(f"Masterpiece Facelift V17 complete: {output_path}")

original_source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png"
theatrical_facelift_v17(original_source, "public/assets/water_deity_unit_final.png")
