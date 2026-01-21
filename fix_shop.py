import cv2
import numpy as np

# Process the new Monster icon
src = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_monster_face_1768961556132.png"
dst = "assets/icon_monster.png"

img = cv2.imread(src, cv2.IMREAD_UNCHANGED)

if img.shape[2] == 3:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

b, g, r, a = cv2.split(img)

# Make black/near-black pixels transparent
black_mask = (r < 25) & (g < 25) & (b < 25)
a[black_mask] = 0

result = cv2.merge([b, g, r, a])
cv2.imwrite(dst, result)
print("Done!")
