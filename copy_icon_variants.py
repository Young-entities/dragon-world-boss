
import shutil
import os

def copy_variants():
    # Copy base (Tight Crop) to circle variant
    # This ensures consistency
    shutil.copy2("public/assets/element_dark.png", "public/assets/element_dark_circle.png")
    shutil.copy2("public/assets/element_holy.png", "public/assets/element_holy_circle.png")
    print("Copied dark/holy base to circle variants.")

copy_variants()
