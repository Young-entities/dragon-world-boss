import cv2
import numpy as np

def surgical_v10_nuke(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return
    
    # 1. Surgical Crop - Remove the outer 10 pixels to kill black corners
    img = img[10:211-12, 10:324-12] 
    h, w = img.shape[:2]

    # 2. Face Processing (304x189 after crop)
    # Face center relative to new crop: x=163-10=153, y=60-10=50
    face_x, face_y = 153, 50
    
    # Sample skin tone
    skin_roi = img[face_y-10:face_y-5, face_x-5:face_x+5]
    skin_color = np.median(skin_roi.reshape(-1, 3), axis=0).astype(np.uint8).tolist()
    
    # Patch Mouth
    cv2.circle(img, (face_x, face_y + 11), 1, skin_color, -1)
    
    # Add Pronounced Nose Shadow
    nose_color = (np.array(skin_color) * 0.7).astype(np.uint8).tolist()
    cv2.circle(img, (face_x, face_y + 4), 1, nose_color, -1)

    # 3. BACKGROUND OBLITERATION (Flood Fill)
    # We use floodFill to target the background more organically
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Fill from corners (0,0) with white background target
    # The checkers are slightly variable, so we use a tolerance
    # Target color is roughly [255, 255, 255] or [239, 239, 239]
    cv2.floodFill(img, mask, (0,0), (255,255,255), (10,10,10), (10,10,10))
    cv2.floodFill(img, mask, (w-1, 0), (255,255,255), (10,10,10), (10,10,10))
    cv2.floodFill(img, mask, (0, h-1), (255,255,255), (10,10,10), (10,10,10))
    # Nuke the bottom right corner (where the 1600 tag is)
    cv2.floodFill(img, mask, (w-1, h-1), (255,255,255), (20,20,20), (20,20,20))

    # 4. Transparency
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Target everything that is now pure white from the floodFill
    bg_mask = (img[:,:,0] > 245) & (img[:,:,1] > 245) & (img[:,:,2] > 245)
    rgba[bg_mask, 3] = 0
    
    # Protect Face Core
    rgba[face_y-15:face_y+20, face_x-10:face_x+10, 3] = 255

    # 5. Upscale (3x)
    final = cv2.resize(rgba, (w*3, h*3), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imwrite(output_path, final)
    print(f"Surgical V10 Nuke completed: {output_path}")

surgical_v10_nuke("C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/uploaded_media_1769312313928.png", "public/assets/water_deity_unit_final.png")
