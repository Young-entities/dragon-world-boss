import cv2
import numpy as np

def surgical_dot_cleanup(input_path, output_path):
    # Load the current icon
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # 1. Edge Refinement
    # The "dot" might be a stray pixel on the edge.
    # We will erode the alpha channel slightly more to cut past any fringe.
    kernel = np.ones((3,3), np.uint8)
    a_refined = cv2.erode(a, kernel, iterations=1)
    
    # 2. Speckle Removal
    # Find any small disconnected "blobs" in the alpha channel and kill them.
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(a_refined)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # If the blob is tiny (like a single pixel or small cluster), it's a "dot"
        if area < 10:
            a_refined[labels == i] = 0
            print(f"Removed artifact speckle of size {area}")

    # 3. High-Intensity Highlight Softening
    # If there's a pure white dot *inside* the crystal that looks like an error, 
    # we can slightly blend it. But usually, it's just the edge.
    
    # Merge back
    result = cv2.merge([b, g, r, a_refined])
    cv2.imwrite(output_path, result)
    print(f"Surgical element cleanup completed: {output_path}")

surgical_dot_cleanup("public/assets/element_fire.png", "public/assets/element_fire_v2.png")
