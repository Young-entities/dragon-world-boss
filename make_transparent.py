import cv2
import numpy as np

# Source icons with black backgrounds
icons = [
    (r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_home_v2_1768960048588.png", "assets/icon_home.png"),
    (r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_battle_v2_1768960061849.png", "assets/icon_battle.png"),
    (r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_monster_v2_1768960077344.png", "assets/icon_monster.png"),
    (r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_equip_v2_1768960092693.png", "assets/icon_equip.png"),
    (r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\icon_shop_v2_1768960119861.png", "assets/icon_shop.png"),
]

for src, dst in icons:
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    
    # Convert to BGRA if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    b, g, r, a = cv2.split(img)
    
    # Make black/near-black pixels transparent
    # Black is where R, G, B are all low (< 30)
    black_mask = (r < 30) & (g < 30) & (b < 30)
    a[black_mask] = 0
    
    result = cv2.merge([b, g, r, a])
    cv2.imwrite(dst, result)
    print(f"Processed: {dst}")

print("Done!")
