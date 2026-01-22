
import re

file_path = 'final_boss_v2.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the const block
# const fullBodyMap = { ... };
# We use dotall to match across lines
pattern = r'const fullBodyMap = \{[^}]*\};'

matches = list(re.finditer(pattern, content))

print(f"Found {len(matches)} occurrences.")

if len(matches) > 1:
    # Get the start and end of the FIRST match (the middle one)
    # The last one is the one we want to keep (at the end of file)
    # Actually, the FIRST one is likely the one I want to remove (the one I tried to comment out)
    # Let's verify positions.
    # We'll just replace the first one.
    
    first_match = matches[0]
    start, end = first_match.span()
    
    new_content = content[:start] + "// Duplicate removed\n" + content[end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Removed first occurrence.")
else:
    print("No duplicates found (or regex mismatch).")
