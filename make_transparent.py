from PIL import Image
import sys

def convert_black_to_transparent(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # If pixel is very dark (black), make it transparent
            # Threshold matches black (#000000) and very dark noise
            if item[0] < 10 and item[1] < 10 and item[2] < 10:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Successfully saved transparent image to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Hardcoded paths based on context
    input_file = r"C:\Users\kevin\.gemini\antigravity\brain\a5b19c6e-530d-45c8-a7ec-27d9452652ae\fire_demon_fixed_black_1768918480522.png"
    output_file = r"c:\Users\kevin\New folder (2)\brave-style-demo\assets\fire_demon_final.png"
    convert_black_to_transparent(input_file, output_file)
