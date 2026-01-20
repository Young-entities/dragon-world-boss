from PIL import Image
import sys

def remove_checkers(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    # Identify checker colors from corners (top-left)
    # Usually checkers are ~20px squares?
    # Or just hardcode common checker colors: White (255) and Light Grey (204 or 192)
    
    # Better approach: Flood Fill from Corners.
    # We can use ImageDraw.floodfill but it needs a seed point and color.
    # Since checkers are alternating, floodfill stops at color change.
    # We need a custom BFS floodfill that tolerates "Checker Pattern".
    
    # Simpler heuristic:
    # If a pixel is (255,255,255) OR (204,204,204) OR (192,192,192) AND it is "outside" the central blob...
    # But "outside" is hard.
    
    # Let's try explicit FloodFill of specific colors starting from 4 corners.
    
    width, height = img.size
    pixels = img.load()
    
    # Set of colors to treat as background (common checkerboard colors)
    bg_colors = set()
    
    # Sample corners to find BG colors
    corners = [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]
    for x,y in corners:
        c = pixels[x,y]
        bg_colors.add(c)
        
    print(f"Detected BG Colors: {bg_colors}")
    
    # Add common ones just in case:
    # (255, 255, 255, 255)
    # (204, 204, 204, 255)
    # (128, 128, 128, 255) - sometimes dark mode checkers
    
    # We will perform BFS from corners. 
    # If a pixel matches ANY color in our "bg_colors" set (or is close to them), we make it transparent.
    # AND add its neighbors to queue.
    
    queue = []
    visited = set()
    
    for x,y in corners:
        queue.append((x,y))
        visited.add((x,y))
        
    processed_count = 0
    
    # Expand bg_colors with variations?
    # Sometimes checkers are not perfect values due to compression.
    # Range check function
    
    def is_bg_color(p):
        r,g,b,a = p
        # Check against known seeds
        for br,bg,bb,ba in bg_colors:
            if abs(r-br) < 10 and abs(g-bg) < 10 and abs(b-bb) < 10:
                return True
        return False

    while queue:
        cx, cy = queue.pop(0)
        current_color = pixels[cx,cy]
        
        # Make transparent
        pixels[cx, cy] = (0, 0, 0, 0)
        processed_count += 1
        
        # Check neighbors
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    neighbor_color = pixels[nx, ny]
                    # If neighbor is one of the BG colors, add to queue
                    if is_bg_color(neighbor_color):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                    # Also, if we hit a "Different" BG color (e.g. going from White square to Grey square)
                    # We need to ensure we don't stop.
                    # The "is_bg_color" check handles this if both colors are in set.
                    # But we might need to dynamically add colors?
                    # If we are at a BG pixel, and neighbor looks like a checker...
                    
                    # Trick: Checkers are usually Grey/White. 
                    # If neighbor is Grey or White, consume it.
                    # Monster is Fire (Red/Black). 
                    # So consume anything Grey/White/Transparent.
                    
                    r,g,b,a = neighbor_color
                    brightness = (r+g+b)/3
                    saturation = 0
                    if max(r,g,b) > 0:
                        saturation = (max(r,g,b) - min(r,g,b)) / max(r,g,b)
                        
                    # Low Clean Grey/White has Low Saturation and High Brightness
                    is_neutral = saturation < 0.1 and brightness > 100
                    
                    if is_neutral:
                         visited.add((nx, ny))
                         queue.append((nx, ny))

    print(f"Processed {processed_count} pixels")
    img.save(output_path, "PNG")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input output")
    else:
        remove_checkers(sys.argv[1], sys.argv[2])
