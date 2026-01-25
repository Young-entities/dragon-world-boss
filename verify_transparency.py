from PIL import Image
import numpy as np

img = Image.open("public/assets/gemini_unit_clean.png")
data = np.array(img)
alpha = data[:,:,3]
transparent_count = np.sum(alpha == 0)
total_count = alpha.size
percent = (transparent_count / total_count) * 100

print(f"Transparency Check:")
print(f"Total Pixels: {total_count}")
print(f"Transparent Pixels (Alpha=0): {transparent_count}")
print(f"Percentage: {percent:.2f}%")

if percent < 5:
    print("Warning: Very little transparency detected. The script might have failed.")
else:
    print("Success: Significant transparency detected.")
