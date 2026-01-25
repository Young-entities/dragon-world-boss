import cv2
import numpy as np

def find_and_nuke_diamond(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    h, w = a.shape
    
    # The diamond is a bright "plus" or "star" shape.
    # It consists of very bright pixels. 
    # Let's find all pixels that are very bright (R,G,B > 200) 
    # and are in the bottom right area.
    
    # Let's search the bottom 40% and right 40% of the image to be absolutely safe.
    search_y = int(h * 0.6)
    search_x = int(w * 0.6)
    
    roi_r = r[search_y:, search_x:]
    roi_g = g[search_y:, search_x:]
    roi_b = b[search_y:, search_x:]
    
    # Threshold for finding the diamond
    # Diamond is usually white/off-white
    binary = ((roi_r > 180) & (roi_g > 180) & (roi_b > 180)).astype(np.uint8) * 255
    
    # Use connected components to find the diamond
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
    
    # The diamond is usually small (e.g. 10x10 to 30x30 pixels)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        width_ = stats[i, cv2.CC_STAT_WIDTH]
        height_ = stats[i, cv2.CC_STAT_HEIGHT]
        
        # Diamond is usually a small, somewhat square-ish or cross-ish area
        if 20 < area < 1000 and 5 < width_ < 60 and 5 < height_ < 60:
            # This is likely the diamond!
            # Nuke it in the alpha channel
            top = stats[i, cv2.CC_STAT_TOP] + search_y
            left = stats[i, cv2.CC_STAT_LEFT] + search_x
            # Wipe a bit larger than the detected box
            a[top-5:top+height_+5, left-5:left+width_+5] = 0
            print(f"Found and Nuked target at y={top}, x={left}")

    # Also hard-clear the absolute bottom-right corner just in case
    a[h-150:, w-150:] = 0
    
    # White background cleanup (the usual)
    is_white = (r > 245) & (g > 245) & (b > 245)
    a[is_white] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(output_path, result)
    print(f"Aggressive Diamond Search & Destroy completed: {output_path}")

find_and_nuke_diamond("public/assets/overlord_white_bg.png", "public/assets/overlord_nuke.png")
