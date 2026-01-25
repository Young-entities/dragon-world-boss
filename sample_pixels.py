from PIL import Image

img = Image.open("public/assets/gemini_unit.png").convert("RGB")
# Check a few points that are likely background
pixels = [
    img.getpixel((0, 0)),
    img.getpixel((10, 10)),
    img.getpixel((0, 10)),
    img.getpixel((10, 0)),
]
print(f"Sample pixels: {pixels}")
