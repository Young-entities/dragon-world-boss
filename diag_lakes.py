import cv2
import numpy as np

def diag_lakes(input_path):
    print(f"Analyzing {input_path}...")
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return

    # Alpha mask
    if img.shape[2] < 4:
        print("No alpha channel found.")
        return
        
    alpha = img[:,:,3]
    h, w = alpha.shape
    
    # Isolate opaque areas
    opaque_mask = (alpha > 200)
    
    # Check color of opaque areas
    b, g, r = cv2.split(img[:,:,:3])
    luma = 0.299*r + 0.587*g + 0.114*b
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    sat = max_c - min_c
    
    # "White Garbage" definition
    is_white_garbage = (luma > 150) & (sat < 30) & opaque_mask
    
    # Find connected components
    garbage_mask = np.zeros((h, w), dtype=np.uint8)
    garbage_mask[is_white_garbage] = 255
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(garbage_mask, 8, cv2.CV_32S)
    
    print("-" * 30)
    print(f"Found {num_labels-1} potential white blobs.")
    print(f"Image Size: {w}x{h}")
    print("Listing Blobs > 10px:")
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids[i][0]), int(centroids[i][1])
        x, y, bw, bh = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        
        if area > 10:
            print(f"Blob #{i}: Area={area} px. Center=({cx},{cy}). Box=[x={x}, y={y}, w={bw}, h={bh}]")

    print("-" * 30)

diag_lakes("public/assets/water_deity_unit_final.png")
