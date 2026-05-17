import re

with open('/Users/yukimichihata/seminar計画/新構成.md', 'r') as f:
    content = f.read()

# Split into parts
ch2_start = content.find('## Chapter 2:')
ch3_start = content.find('## Chapter 3:')

before_ch2 = content[:ch2_start]
ch2_content = content[ch2_start:ch3_start]
after_ch2 = content[ch3_start:]

# Inside ch2_content, we want to extract the sections and reorder them.
# The sections are split by '### '
sections = re.split(r'(?=### \d{2} / )', ch2_content)

# sections[0] is the chapter header and description
header = sections[0]
sec_09 = sections[1] # 09 / 成果地点
sec_10 = sections[2] # 10 / 経営課題
sec_11 = sections[3] # 11 / 顧客仮説
sec_12 = sections[4] # 12 / 競合設定
sec_13 = sections[5] # 13 / CV構造
sec_14 = sections[6] # 14 / 成果モデル別
sec_15 = sections[7] # 15 / コラム
sec_16 = sections[8] # 16 / マイクロCV

# We want the order: 09, 10, 13, 14, 16, 15, 11, 12
# And we need to renumber them.
new_sections = [
    sec_09, # 09
    sec_10, # 10
    sec_13, # 11 (was 13)
    sec_14, # 12 (was 14)
    sec_16, # 13 (was 16)
    sec_15, # 14 (was 15)
    sec_11, # 15 (was 11)
    sec_12  # 16 (was 12)
]

# Update the chapter header
header = header.replace('成果地点 → 顧客仮説 → 計測設計（6枚）', '成果地点 → 計測設計 → 顧客仮説（8枚）')
header = header.replace('「誰の・何の成果を・どう測るか」', '「何の成果を・どう測り・誰から得るか」')
header = header.replace('（成果地点・顧客仮説・CV構造）', '（成果地点・CV構造・顧客仮説）')

# Update "2つ目の問い" and "3つ目の問い"
for i, s in enumerate(new_sections):
    if 'CV構造と計測の基本' in s:
        new_sections[i] = s.replace('**3つ目の問い**', '**2つ目の問い**')
    if '顧客仮説 — ペルソナとジャーニー' in s:
        new_sections[i] = s.replace('**2つ目の問い**', '**3つ目の問い**')

# Update numbering for all sections
for i in range(len(new_sections)):
    # Replace the starting number
    new_num = f"{i+9:02d}"
    new_sections[i] = re.sub(r'^### \d{2}', f'### {new_num}', new_sections[i])

new_ch2_content = header + "".join(new_sections)

with open('/Users/yukimichihata/seminar計画/新構成.md', 'w') as f:
    f.write(before_ch2 + new_ch2_content + after_ch2)

print("Done")
