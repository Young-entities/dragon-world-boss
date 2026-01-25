from PIL import Image
import numpy as np

def sample_comprehensive(input_path):
    img = Image.open(input_path).convert("RGB")
    data = np.array(img)
    # Sample top-left corner area (10x10) to see background colors
    corner = data[0:10, 0:10]
    unique_colors = np.unique(corner.reshape(-1, 3), axis=0)
    print("Unique colors in top-left 10x10:")
    for c in unique_colors:
        print(tuple(c))

sample_comprehensive("public/assets/gemini_unit.png")
