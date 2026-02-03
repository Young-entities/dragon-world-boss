
import os

def check_nature():
    files = [
        "public/assets/element_earth.png",
        "public/assets/element_earth_circle.png",
        "public/assets/element_grass.png",
        "public/assets/element_grass_circle.png"
    ]
    for f in files:
        print(f"{f}: {os.path.exists(f)}")

check_nature()
