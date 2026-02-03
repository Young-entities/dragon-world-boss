
import cv2
import os

def check_gen_size():
    path = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/earth_unit_gen_v7_1769797134960.png"
    img = cv2.imread(path)
    if img is not None:
        print(f"Size: {img.shape[1]}x{img.shape[0]}")
    else:
        print("Not found")

check_gen_size()
