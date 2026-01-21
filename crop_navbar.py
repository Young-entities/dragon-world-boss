import cv2
import numpy as np

# Read the original image
img = cv2.imread(r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\navbar_wide_1768960666152.png")

# Get dimensions
h, w = img.shape[:2]

# Crop the bottom portion where the navbar is (approximately bottom 40%)
navbar_start = int(h * 0.45)
navbar = img[navbar_start:h, :]

# Save it
cv2.imwrite("assets/navbar_bg.png", navbar)
print(f"Cropped navbar: {navbar.shape[1]}x{navbar.shape[0]}")
