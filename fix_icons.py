import cv2
import numpy as np
import os

# Icon files to process
icons = ['icon_home.png', 'icon_battle.png', 'icon_monster.png', 'icon_equip.png', 'icon_shop.png']
assets_dir = 'assets'

for icon in icons:
    path = os.path.join(assets_dir, icon)
    if not os.path.exists(path):
        print(f"Skipping {icon} - not found")
        continue
    
    # Read with alpha
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    
    # Convert to BGRA if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Get the checkered grey color (around 191-204 for light, 178-191 for dark)
    # Make anything that's close to grey checkered pattern transparent
    b, g, r, a = cv2.split(img)
    
    # Grey detection - where R, G, B are all similar and in the grey range
    grey_mask = (
        (np.abs(r.astype(int) - g.astype(int)) < 20) & 
        (np.abs(g.astype(int) - b.astype(int)) < 20) &
        (r > 150) & (r < 220)
    )
    
    # Set alpha to 0 for grey pixels
    a[grey_mask] = 0
    
    # Merge back
    result = cv2.merge([b, g, r, a])
    
    # Save
    cv2.imwrite(path, result)
    print(f"Processed {icon}")

print("Done!")
