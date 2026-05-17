import os

def replace_css_in_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 最初の <style> と </style> を探す
    # 様々なインデントに対応
    import re
    pattern = re.compile(r'\s*<style>.*?</style>', re.DOTALL)
    
    match = pattern.search(content)
    if match:
        # 置換する
        new_content = pattern.sub('\n  <link rel="stylesheet" href="style.css">', content, count=1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully replaced CSS block with stylesheet link in {file_path}")
    else:
        print(f"Could not find <style> block in {file_path}")

replace_css_in_file('/Users/yukimichihata/seminar計画/itc_tutorial_slides.template.html')
replace_css_in_file('/Users/yukimichihata/seminar計画/itc_tutorial_slides.html')
