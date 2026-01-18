
from PIL import Image
import numpy as np

def remove_white(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # White is (255, 255, 255)
    red, green, blue, alpha = data.T
    
    # Define what "white" is (e.g. brighter than 220)
    white_areas = (red > 220) & (green > 220) & (blue > 220)
    
    # Set alpha to 0 for white areas
    data[..., 3][white_areas.T] = 0
    
    # Save
    new_img = Image.fromarray(data)
    new_img.save(output_path)
    print(f"Saved transparent image to {output_path}")

try:
    remove_white("fire_dragon.jpg", "fire_dragon_transparent.png")
except Exception as e:
    print(f"Error: {e}")
