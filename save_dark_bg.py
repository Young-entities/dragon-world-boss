import shutil
import os

source = "C:/Users/kevin/.gemini/antigravity/brain/81d8f95f-2fb1-4581-be59-77f60b477988/dark_void_background_1769702147823.png"
dest = "public/assets/dark_void_bg.png"

try:
    shutil.copy(source, dest)
    print(f"Background Saved: {dest}")
except Exception as e:
    print(f"Error: {e}")
