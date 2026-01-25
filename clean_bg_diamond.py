import cv2
import numpy as np

def find_and_nuke_bg_diamond(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
    
    h, w = img.shape[:2]
    
    # Target the bottom right area of the BACKGROUND
    search_y = int(h * 0.7)
    search_x = int(w * 0.7)
    
    roi = img[search_y:, search_x:]
    b, g, r = cv2.split(roi)
    
    # Look for bright neutral sparkles
    # Standard AI diamond is often very bright (250+)
    binary = ((r > 200) & (g > 200) & (b > 200)).astype(np.uint8) * 255
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # Diamond is usually small
        if area < 2000:
            top = stats[i, cv2.CC_STAT_TOP] + search_y
            left = stats[i, cv2.CC_STAT_LEFT] + search_x
            height_ = stats[i, cv2.CC_STAT_HEIGHT]
            width_ = stats[i, cv2.CC_STAT_WIDTH]
            
            # Fill with surrounding-like colors or just blur it out
            # For simplicity, let's just make it a patch of the average surrounding color
            # or just blur it heavily. 
            # Actually, let's just use the median of the area's surroundings.
            roi_plus = img[max(0, top-20):min(h, top+height_+20), max(0, left-20):min(w, left+width_+20)]
            if roi_plus.size > 0:
                avg_color = np.median(roi_plus.reshape(-1, 3), axis=0)
                img[top:top+height_, left:left+width_] = avg_color
            print(f"Removed background artifact at y={top}, x={left}")

    # Also hard-clear the absolute bottom-right corner pixel clusters
    # AI logos are often literally in the corner.
    # Wiping a tiny 60x60 corner to match the ground color.
    corner_avg = np.median(img[h-100:h-80, w-100:w-80].reshape(-1, 3), axis=0)
    img[h-80:, w-80:] = corner_avg

    cv2.imwrite(output_path, img)
    print(f"Cleaned background saved to {output_path}")

find_and_nuke_bg_diamond("public/assets/gemini_bg.png", "public/assets/gemini_bg_clean.png")
