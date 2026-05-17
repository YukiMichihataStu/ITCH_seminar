import os

template_path = '/Users/yukimichihata/seminar計画/itc_tutorial_slides.template.html'
css_path = '/Users/yukimichihata/seminar計画/style.css'

with open(template_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# <style> is at line 14 (index 13)
# </style> is at line 1486 (index 1485)
# CSS content is index 14 to 1485
css_lines = lines[14:1485]
css_content = "".join(css_lines)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print(f"Successfully extracted {len(css_lines)} lines of CSS to {css_path}")
