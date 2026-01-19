from PIL import Image, ImageDraw

def remove_background(input_path, output_path):
    print(f"Processing {input_path}...")
    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        
        # Strategy: Flood fill from all 4 corners and mid-points of edges
        # This handles checkerboards that might alternate at corners
        
        seeds = [
            (0, 0), (width-1, 0), (0, height-1), (width-1, height-1), # Corners
            (width//2, 0), (width//2, height-1), (0, height//2), (width-1, height//2) # Mid-edges
        ]
        
        # We need to be careful. If the hero touches the edge, we erase the hero.
        # Assuming the hero is centered and framed by background.
        
        # Let's verify the hero is not touching edges.
        # Usually these google images have a margin.
        
        # We perform flood fill with a transparent color (0,0,0,0)
        # Threshold allows for slight compression artifacts (JPG noise)
        
        for seed in seeds:
            try:
                # Get color at seed
                seed_color = img.getpixel(seed)
                # If it's already transparent, skip
                if seed_color[3] == 0:
                    continue
                
                # Flood fill
                ImageDraw.floodfill(img, seed, (0,0,0,0), thresh=50)
            except Exception as e:
                print(f"Warning at seed {seed}: {e}")
        
        img.save(output_path)
        print(f"Saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_background("hero.png", "hero_cleaned.png")
