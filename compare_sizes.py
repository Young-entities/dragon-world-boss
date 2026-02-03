
import cv2

def check_size(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"{path}: Not Found")
        return
    h, w = img.shape[:2]
    print(f"{path}: {w}x{h}")
    
    # Check bounding box (content size)
    if img.shape[2] == 4:
        a = img[:, :, 3]
        coords = cv2.findNonZero(a)
        if coords is not None:
            x, y, cw, ch = cv2.boundingRect(coords)
            print(f"  Content: {cw}x{ch} (Offset: {x},{y})")
            print(f"  Padding: Left:{x}, Right:{w-(x+cw)}, Top:{y}, Bottom:{h-(y+ch)}")

check_size("public/assets/dark_deity_unit_v4.png")
check_size("public/assets/celestial_valkyrie.png")
