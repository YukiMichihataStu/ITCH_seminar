#!/usr/bin/env python3
"""
itc_tutorial_slides.html を各チャプターごとのHTMLフラグメントに分割する。

方針: BeautifulSoupに頼らず、<div class="template-block"> のネストを手動追跡。
"""

import re
from pathlib import Path

SOURCE = Path("itc_tutorial_slides.html")
OUT_DIR = Path("slides")


def extract_blocks(html: str) -> list[dict]:
    """HTMLから各 template-block を正確に切り出す"""
    blocks = []
    lines = html.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # template-block 開始タグを検出
        if '<div class="template-block">' in line:
            # この行から前に遡ってコメントブロックを取得
            comment_lines = []
            j = i - 1
            while j >= 0:
                prev = lines[j].strip()
                if prev == '':
                    j -= 1
                    continue
                if '<!--' in lines[j] and '==' in lines[j]:
                    # コメントブロック行を収集
                    while j >= 0 and ('==' in lines[j] or 'SLIDE' in lines[j] or 
                                      'CHAPTER' in lines[j] or 'APPENDIX' in lines[j] or
                                      'CSV' in lines[j]):
                        comment_lines.insert(0, lines[j])
                        j -= 1
                    break
                else:
                    break
            
            # template-block の終了を検出（divネスト追跡）
            depth = 0
            block_lines = list(comment_lines)
            k = i
            while k < len(lines):
                block_lines.append(lines[k])
                depth += lines[k].count('<div')
                depth -= lines[k].count('</div>')
                if depth <= 0:
                    break
                k += 1
            
            content = '\n'.join(block_lines)
            
            # ラベルを取得
            label_match = re.search(r'<div class="label">(.*?)</div>', content)
            label = label_match.group(1) if label_match else "unknown"
            
            blocks.append({
                'label': label,
                'content': content,
            })
            
            i = k + 1
        else:
            i += 1
    
    return blocks


def categorize_blocks(blocks: list[dict]) -> dict[str, list[dict]]:
    """ブロックをチャプターごとに分類する"""
    chapters = {
        '00_intro': [],
        '01_common_understanding': [],
        '02_goal_measurement': [],
        'appendix': [],
    }
    
    for block in blocks:
        label = block['label']
        
        # APPENDIX判定
        if 'APPENDIX' in label:
            chapters['appendix'].append(block)
        # Chapter 1扉 + その中身 (05〜07)
        elif 'チャプター扉 — Webマーケの共通理解' in label:
            chapters['01_common_understanding'].append(block)
        elif label.startswith(('05 ', '06 ', '07 ')):
            chapters['01_common_understanding'].append(block)
        # Chapter 2扉 + その中身 (08〜17)
        elif 'チャプター扉 — 成果地点' in label:
            chapters['02_goal_measurement'].append(block)
        elif label.startswith(('08 ', '09 ')):
            chapters['02_goal_measurement'].append(block)
        elif re.match(r'^1[0-9] ', label):
            chapters['02_goal_measurement'].append(block)
        # 導入 (01〜04)
        elif label.startswith(('01 ', '02 ', '03 ', '04 ')):
            chapters['00_intro'].append(block)
        else:
            print(f"  [⚠️WARN] 未分類ブロック: {label}")
            chapters['00_intro'].append(block)
    
    return chapters


def main():
    html = SOURCE.read_text(encoding='utf-8')
    
    blocks = extract_blocks(html)
    
    print(f"[ℹ️INFO] 抽出されたブロック数: {len(blocks)}")
    for b in blocks:
        print(f"  - {b['label']}")
    
    chapters = categorize_blocks(blocks)
    
    OUT_DIR.mkdir(exist_ok=True)
    
    for filename, chapter_blocks in chapters.items():
        if not chapter_blocks:
            continue
        
        content = "\n\n".join(b['content'] for b in chapter_blocks)
        outpath = OUT_DIR / f"{filename}.html"
        outpath.write_text(content + "\n", encoding='utf-8')
        
        labels = [b['label'] for b in chapter_blocks]
        print(f"[✅SUCCESS] {outpath} ({len(chapter_blocks)} blocks)")
        for l in labels:
            print(f"    📄 {l}")
    
    print(f"\n[ℹ️INFO] 分割完了！")
    for f in sorted(OUT_DIR.glob("*.html")):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
