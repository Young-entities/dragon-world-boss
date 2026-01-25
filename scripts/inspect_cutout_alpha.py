from pathlib import Path
from PIL import Image
import numpy as np

cutout = Path(r"C:\Users\kevin\New folder (2)\monster-warlord\public\assets\unit_cutout.png")
img = Image.open(cutout).convert("RGBA")
alpha = np.array(img)[:, :, 3]
print("alpha min:", int(alpha.min()), "max:", int(alpha.max()), "nonzero:", int((alpha > 0).sum()))
