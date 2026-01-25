import cv2
import numpy as np

def create_water_element(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return

    # Split channels
    b, g, r, a = cv2.split(img)

    # Convert to HSV to rotate colors
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Fire is around 0-30 hue. Water is around 100-140.
    # Shift hue by about 100-120
    h_new = (h.astype(np.int32) + 110) % 180
    h_new = h_new.astype(np.uint8)

    # Boost saturation for a nice deep blue
    s_new = cv2.add(s, 40)

    # Merge HSV back
    water_hsv = cv2.merge([h_new, s_new, v])
    water_bgr = cv2.cvtColor(water_hsv, cv2.COLOR_HSV2BGR)

    # Combine with original alpha
    wb, wg, wr = cv2.split(water_bgr)
    result = cv2.merge([wb, wg, wr, a])

    cv2.imwrite(output_path, result)
    print(f"Water Element Icon created: {output_path}")

create_water_element("public/assets/element_fire_v4.png", "public/assets/element_water.png")
