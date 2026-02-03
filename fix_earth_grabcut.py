
import cv2
import numpy as np

def fix_earth_grabcut():
    src = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_white_bg_1769803384079.png"
    out = "public/assets/earth_minion.png"
    
    print(f"Fixing Earth Unit with GrabCut from {src}...")
    
    img = cv2.imread(src)
    if img is None:
        return
        
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    
    # Define Rect (Assume unit is centered, with margin)
    h, w = img.shape[:2]
    # Margin 5 pixels
    rect = (5, 5, w-10, h-10)
    
    # GrabCut
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    # Mask: 0=BG, 1=FG, 2=ProbBG, 3=ProbFG
    # We take 1 and 3 as Foreground
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # Add Alpha
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = mask2 * 255
    
    cv2.imwrite(out, img)
    print(f"Saved {out} (GrabCut)")

fix_earth_grabcut()
