import cv2
import numpy as np

def seamless_bg_fix(input_path, output_path):
    # Read the original background
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not find {input_path}")
        return
    
    h, w = img.shape[:2]
    
    # 1. Create a mask specifically for the diamond
    # Based on the previous successful detection at y=704, x=1126
    # and looking at the latest user screenshot.
    mask = np.zeros((h, w), np.uint8)
    
    # Target the artifact in the bottom-right quadrant
    search_y = int(h * 0.7)
    search_x = int(w * 0.7)
    roi = img[search_y:, search_x:]
    b, g, r = cv2.split(roi)
    
    # Find the bright sparkle
    binary = ((r > 190) & (g > 190) & (b > 190)).astype(np.uint8) * 255
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] < 3000:
            top = stats[i, cv2.CC_STAT_TOP] + search_y
            left = stats[i, cv2.CC_STAT_LEFT] + search_x
            height_ = stats[i, cv2.CC_STAT_HEIGHT]
            width_ = stats[i, cv2.CC_STAT_WIDTH]
            # Draw on our global mask
            mask[top-5:top+height_+5, left-5:left+width_+5] = 255
            print(f"Masked artifact at y={top}, x={left}")

    # 2. SEAMLESS INPAINTING
    # This uses Telea's algorithm to fill the masked area based on surrounding textures
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # Also handle the absolute corner if anything remains
    # instead of a flat box, we'll use a tiny inpaint circle if needed.
    # But current mask should catch it.
    
    cv2.imwrite(output_path, result)
    print(f"Seamlessly cleaned background saved to {output_path}")

seamless_bg_fix("public/assets/gemini_bg.png", "public/assets/gemini_bg_clean.png")
