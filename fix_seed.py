import re
import urllib.parse

with open('seed.py', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_product_img(match):
    block = match.group(0)
    name_match = re.search(r"name='([^']+)'", block)
    if not name_match:
        return block
    
    name = name_match.group(1)
    short_name = "\\n".join(name.split()[:3]) # Use newlines for better placeholder text fit
    encoded = urllib.parse.quote(short_name)
    new_url = f"https://placehold.co/600x600/f4f4f4/00acc1?text={encoded}"
    
    new_block = re.sub(r"image_url='[^']+'", f"image_url='{new_url}'", block)
    return new_block

new_content = re.sub(r"Product\([^)]+\)", replace_product_img, content)

with open('seed.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Updated seed.py successfully")
