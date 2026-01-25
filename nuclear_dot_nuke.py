import cv2
import numpy as np

def nuclear_dot_nuke(input_path, output_path):
    # Load the icon
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # 1. Target the internal white dot
    # We look for pixels that are very bright (almost pure white/yellow)
    # inside the area where the fire is. 
    # Usually these artifacts have R, G, B > 240
    white_mask = (r > 240) & (g > 240) & (b > 240)
    
    # We don't want to kill the whole flame, just the tiny "dot"
    # So we use connected components to find small bright blobs
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(white_mask.astype(np.uint8) * 255)
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # Any bright white blob smaller than 15 pixels is definitely a "dot" artifact
        if 1 <= area < 15:
            # We "patch" it by taking the color from a neighbor (e.g. 2 pixels to the right)
            top = stats[i, cv2.CC_STAT_TOP]
            left = stats[i, cv2.CC_STAT_LEFT]
            # Replace the dot area with surrounding fire color
            # Just take the median of the surrounding 5x5 area
            roi = img[max(0, top-5):min(img.shape[0], top+10), max(0, left-5):min(img.shape[1], left+10)]
            if roi.size > 0:
                avg_color = np.median(roi.reshape(-1, 4), axis=0)
                img[labels == i] = avg_color
            print(f"Nuked internal white dot artifact of size {area}")

    # 2. Hard mask the circular edge again just to be absolute
    h, w = a.shape
    center = (w // 2, h // 2)
    # Cut slightly deeper (42% radius instead of 44%) to kill any edge-dots
    radius = int(min(h, w) * 0.42)
    mask = np.zeros((h, w), np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    # Kill everything outside the smaller circle
    img[:, :, 3] = cv2.bitwise_and(img[:, :, 3], mask)
    
    # Final smoothing
    img[:, :, 3] = cv2.GaussianBlur(img[:, :, 3], (3,3), 0)

    cv2.imwrite(output_path, img)
    print(f"Absolute Nuclear Cleanup completed: {output_path}")

nuclear_dot_nuke("public/assets/icon_fire_raw.png", "public/assets/element_fire_v3.png")
