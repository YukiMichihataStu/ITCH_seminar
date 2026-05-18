import bs4
import re
import copy

def main():
    html_path = 'itc_tutorial_slides.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = bs4.BeautifulSoup(f, 'html.parser')

    # テンプレートブロック抽出
    blocks = soup.find_all('div', class_='template-block')
    templates = {}
    for block in blocks:
        section = block.find('section')
        if not section: continue
        classes = section.get('class', [])
        t_type = 'v-slide'
        for c in classes:
            if c.startswith('v-'):
                t_type = c
                break
        if t_type not in templates:
            templates[t_type] = copy.copy(block)
    
    # 既存スライドをすべて削除
    for block in blocks:
        block.decompose()
        
    body = soup.find('body')

    page_counter = 1
    total_pages = 40 # 目安

    def create_slide(label, template_type, modifier_func):
        nonlocal page_counter
        new_block = copy.copy(templates[template_type])
        
        # label
        label_div = new_block.find('div', class_='label')
        if label_div: label_div.string = f"{page_counter:02d} / {label}"
            
        # header 
        title = new_block.find('h1', class_='slide-heading')
        if title: title.string = label
        
        # ページ番号
        page_num = new_block.find('span', class_='page-num')
        if page_num: page_num.string = f"{page_counter:02d} / {total_pages}"
        
        # 中身のクリアや基本処理
        modifier_func(new_block)
        
        body.insert(len(body.contents) - 1, new_block)
        body.append("\n\n")
        page_counter += 1

    # --- 導入 ---
    def mod_01(b): pass
    create_slide("タイトル", "v-cover", mod_01)

    def mod_02(b): pass
    create_slide("本研修の目的", "v-do-dont", mod_02)

    def mod_03(b): pass
    create_slide("今日の整理順", "v-flow-map", mod_03)

    def mod_04(b): pass
    create_slide("自己紹介", "v-summary", mod_04)

    def mod_05(b):
        title = b.find('h1', class_='slide-heading')
        if title: title.string = "この3つが揃えば伴走支援は「OK」"
        box = b.find('div', class_='trap-message-box')
        if box:
            h2 = box.find('h2')
            if h2: h2.string = "伴走支援の合格基準"
            items = box.find_all('div', style=re.compile("background: var\(--accent-soft\)"))
            if len(items) >= 2:
                items[0].find('h3').string = "① 課題を掴めている"
                items[0].find('p').string = "「お客さんは何がしたくて、どこで詰まってるか」を整理できていること。"
                items[1].find('h3').string = "② 課題と施策が一致している"
                items[1].find('p').string = "解決したい課題に対して、選んだ手段（施策）が最短距離になっていること。"
                third = copy.copy(items[1])
                third.find('h3').string = "③ 測れる状態にしている"
                third.find('p').string = "数字でどこが詰まっているかを見る基盤があること。"
                items[1].insert_after(third)
    create_slide("この3つが揃えば伴走支援は「OK」", "v-problem-trap", mod_05)

    # --- Ch1 ---
    def mod_06(b):
        b.find('div', class_='chapter-number').string = "01"
        b.find('h1', class_='chapter-title').string = "Ch1：課題を掴む"
        b.find('p', class_='chapter-body').string = "「お客さんは何がしたくて、どこで詰まってるか」を整理する\n\nITCのスキル：課題特定力・整理力を活かすフェーズです。"
    create_slide("Ch1扉", "v-chapter", mod_06)

    def mod_07(b):
        b.find('h1', class_='slide-heading').string = "成果モデルの整理（MELSA）"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
    create_slide("成果モデルの整理（MELSA）", "v-model-table", mod_07)

    def mod_08(b):
        b.find('h1', class_='slide-heading').string = "ボトルネック3大分類"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
    create_slide("ボトルネック3大分類", "v-phases", mod_08)

    def mod_09(b):
        b.find('h1', class_='slide-heading').string = "数字で見る「どこで止まってるか」"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
    create_slide("数字で見る「どこで止まってるか」", "v-funnel", mod_09)

    def mod_10(b):
        b.find('h1', class_='slide-heading').string = "リードモデルのKPI例"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<table class="data-table" style="font-size: 11px;">
  <thead>
    <tr><th>指標</th><th>マッチングA</th><th>パートナーB</th><th>自社サイト</th><th>全体</th></tr>
  </thead>
  <tbody>
    <tr><td>潜在顧客</td><td>8,000</td><td>2,000</td><td>800</td><td>10,800</td></tr>
    <tr><td>訪問者</td><td>500</td><td>500</td><td>200</td><td>1,200</td></tr>
    <tr><td>CV（問い合わせ）</td><td>100</td><td>20</td><td>40</td><td>160</td></tr>
    <tr><td>商談</td><td>20</td><td>8</td><td>8</td><td>36</td></tr>
    <tr><td>顧客</td><td>5</td><td>4</td><td>2</td><td>11</td></tr>
    <tr style="background: rgba(0, 114, 206, 0.05);"><td>訪問率</td><td style="color:var(--signal);font-weight:700">6.25%</td><td>25.0%</td><td>25.0%</td><td>-</td></tr>
    <tr style="background: rgba(21, 99, 86, 0.05);"><td>CVR</td><td>20.0%</td><td style="color:var(--signal);font-weight:700">4.0%</td><td>20.0%</td><td>-</td></tr>
    <tr><td>商談率</td><td>20.0%</td><td style="color:var(--ok);font-weight:700">40.0%</td><td>20.0%</td><td>-</td></tr>
    <tr><td>受注率</td><td>25.0%</td><td style="color:var(--ok);font-weight:700">50.0%</td><td>25.0%</td><td>-</td></tr>
  </tbody>
</table>
<div style="margin-top: 12px; font-size: 13px;">
  <p>→ マッチングAは訪問率6.25%で低いが、CVRは20%で優秀 ＝ <strong>流入の質に課題</strong></p>
  <p>→ パートナーBはCVR4%で低いが、商談化率40%で優秀 ＝ <strong>サイトの受け皿に課題</strong></p>
  <p>→ リードモデルではCVの先（商談→受注）まで追うことが重要</p>
</div>
''', 'html.parser'))
    create_slide("リードモデルのKPI例", "v-model-table", mod_10)

    def mod_11(b):
        b.find('h1', class_='slide-heading').string = "ECモデルのKPI例"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<table class="data-table" style="font-size: 11px;">
  <thead>
    <tr><th>指標</th><th>モールA</th><th>フリマB</th><th>自社サイト</th><th>全体</th></tr>
  </thead>
  <tbody>
    <tr><td>全ユーザー</td><td>40,000</td><td>30,000</td><td>6,000</td><td>76,000</td></tr>
    <tr><td>商品一覧</td><td>3,000</td><td>15,000</td><td>3,000</td><td>21,000</td></tr>
    <tr><td>商品詳細</td><td>300</td><td>300</td><td>300</td><td>900</td></tr>
    <tr><td>カート</td><td>30</td><td>30</td><td>30</td><td>90</td></tr>
    <tr><td>CV（購入）</td><td>6</td><td>6</td><td>6</td><td>18</td></tr>
    <tr style="background: rgba(0, 114, 206, 0.05);"><td>商品一覧到達率</td><td style="color:var(--signal);font-weight:700">7.5%</td><td>50.0%</td><td>50.0%</td><td>-</td></tr>
    <tr style="background: rgba(21, 99, 86, 0.05);"><td>商品詳細到達率</td><td>10.0%</td><td style="color:var(--signal);font-weight:700">2.0%</td><td>10.0%</td><td>-</td></tr>
    <tr><td>カート到達率</td><td>10.0%</td><td>10.0%</td><td>10.0%</td><td>-</td></tr>
    <tr><td>CVR</td><td>20.0%</td><td>20.0%</td><td>20.0%</td><td>-</td></tr>
  </tbody>
</table>
<div style="margin-top: 12px; font-size: 13px;">
  <p>→ モールAは商品一覧到達率が極端に低い（7.5%）＝ <strong>集客の質の問題</strong></p>
  <p>→ フリマBは商品詳細到達率が2.0% ＝ <strong>一覧→詳細の導線問題</strong></p>
  <p>→ このように「どのステップで詰まるか」でボトルネックと打ち手が変わる</p>
</div>
''', 'html.parser'))
    create_slide("ECモデルのKPI例", "v-model-table", mod_11)

    def mod_12(b):
        b.find('h1', class_='slide-heading').string = "💡 さらに解像度を上げる：自社サイトの流入チャネル別分解"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<p style="font-size:13px; margin-bottom:12px;">自社サイト全体の数字だけを見ても課題は見えにくい。「どこから来たか（流入元）」で分解すると、打つべき施策がより明確になる。</p>
<table class="data-table" style="font-size: 11px;">
  <thead>
    <tr><th>指標</th><th>オーガニック検索</th><th>広告</th><th>SNS経由</th><th>全体（自社サイト）</th></tr>
  </thead>
  <tbody>
    <tr><td>訪問者</td><td>1,000</td><td>500</td><td>1,500</td><td>3,000</td></tr>
    <tr><td>CV（問い合わせ）</td><td>20</td><td>25</td><td>3</td><td>48</td></tr>
    <tr style="background: rgba(21, 99, 86, 0.05);"><td>CVR</td><td>2.0%</td><td style="color:var(--ok);font-weight:700">5.0%</td><td style="color:var(--signal);font-weight:700">0.2%</td><td>1.6%</td></tr>
  </tbody>
</table>
<div style="margin-top: 12px; font-size: 13px; line-height:1.6;">
  <p>→ <strong>全体CVRは1.6%</strong>だが、中身は全く違う。</p>
  <p>→ <strong>SNS経由</strong>は訪問者が多いがCVR0.2%。課題は「興味本位のユーザーばかりで、問い合わせる気がない」こと（＝<strong>集客の質</strong>）。</p>
  <p>→ <strong>リスティング広告</strong>はCVR5.0%と優秀。課題は「もっと予算をかけて訪問者を増やせないか？」（＝<strong>集客の量</strong>）。</p>
  <p>→ 流入元を分解しないと、「全体のCVRを上げよう」という<strong>見当違いの打ち手</strong>になってしまう可能性がある。</p>
</div>
''', 'html.parser'))
    create_slide("自社サイトの流入チャネル別分解", "v-model-table", mod_12)

    def mod_13(b):
        b.find('h1', class_='slide-heading').string = "Ch1のまとめ：課題を掴む"
        b.find('span', class_='section-badge').string = "CHAPTER 01"
        p = b.find('div', class_='summary-points')
        if p:
            p.replace_with(bs4.BeautifulSoup('''
<ul class="split-list" style="margin-top: 20px; font-size: 16px;">
  <li><span class="icon-symbol" style="color:var(--accent)">check_circle</span>成果モデルを決める</li>
  <li><span class="icon-symbol" style="color:var(--accent)">check_circle</span>ボトルネックを「集客 / 理解・信頼 / 行動」に分ける</li>
  <li><span class="icon-symbol" style="color:var(--accent)">check_circle</span>数字でどこが詰まっているかを見る</li>
</ul>
<p style="margin-top:20px; font-size:14px; color:var(--muted)">※月間目標やチャネル別の予算設計は応用編としてAPPENDIXで扱います。</p>
''', 'html.parser'))
    create_slide("Ch1のまとめ", "v-summary", mod_13)

    # --- Ch2 ---
    def mod_14(b):
        b.find('div', class_='chapter-number').string = "02"
        b.find('h1', class_='chapter-title').string = "Ch2：施策を整理する"
        b.find('p', class_='chapter-body').string = "Ch1で「どこで詰まっているか」を掴んだら、次は「その詰まりに何をぶつけるか」を整理します。\n全体像を見渡す → 広告で連れてくる → LPで受け止める → 効いてるか見る。"
    create_slide("Ch2扉", "v-chapter", mod_14)

    def mod_15(b):
        b.find('h1', class_='slide-heading').string = "施策マップ俯瞰：全体像をまず見渡す"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<p style="font-size:13px; margin-bottom:12px;">Ch1で整理した「どこで詰まっているか」から、打ち手を発想します。主軸はあくまで<strong>ボトルネック別</strong>に考えること。<br>補助金申請では、ここで施策を「何を発注するか」「どの補助科目に入るか」に翻訳していきます。</p>
<table class="data-table" style="font-size: 11px;">
  <thead>
    <tr><th>ボトルネック</th><th>施策の方向性</th><th>施策例</th><th>予算の受け皿（補助科目）</th></tr>
  </thead>
  <tbody>
    <tr><td>集客：[PV]そもそも来てない</td><td>流入を増やす</td><td>検索広告・SNS広告・SEO・MEO・チラシ・ポータル掲載</td><td>オ. 広告宣伝費 / イ. サイト構築費（SEO）</td></tr>
    <tr><td>理解・信頼：[PV→CV]来てるけど離脱</td><td>受け皿を整える</td><td>LP改善・事例・FAQ・写真・口コミ・コンテンツ充実</td><td>イ. サイト構築費 / ウ. コンテンツ制作費</td></tr>
    <tr><td>行動：[CVR]あと一歩で逃げる</td><td>背中を押す</td><td>CTA改善・フォーム最適化（EFO）・導線追加・リターゲティング</td><td>イ. サイト構築費（改修） / オ. 広告宣伝費（リターゲ）</td></tr>
  </tbody>
</table>
<p style="font-size:12px; margin-top:12px; color:var(--muted)">施策は多岐にわたるため、すべてを紹介するのではなく、補助金申請や発注仕様に落としやすい重要項目を中心に扱います。</p>
''', 'html.parser'))
    create_slide("施策マップ俯瞰", "v-model-table", mod_15)

    def mod_16(b):
        b.find('h1', class_='slide-heading').string = "参考：施策の性質を「顕在層 / 潜在層」で見る"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<p style="font-size:13px; margin-bottom:12px;">同じ「集客」でも、今すぐ客を取りにいく施策と、まだ検討前の人に知ってもらう施策では、成果の出方が違います。</p>
<table class="data-table" style="font-size: 12px;">
  <thead>
    <tr><th>分類</th><th>顧客の状態</th><th>代表的な施策</th></tr>
  </thead>
  <tbody>
    <tr><td>顕在層向き</td><td>今すぐ欲しい・探している</td><td>検索広告・SEO・MEO</td></tr>
    <tr><td>潜在層向き</td><td>まだ気づいていない・比較検討前</td><td>ディスプレイ広告・動画広告・SNS広告・コンテンツマーケ</td></tr>
    <tr><td>両方</td><td>接点を持った人を追いかける</td><td>リターゲティング・メルマガ</td></tr>
  </tbody>
</table>
<ul style="font-size:13px; margin-top:16px; line-height:1.6; padding-left:20px;">
  <li>顕在層向き施策は<strong>CVRが高い</strong>が<strong>母数が小さい</strong></li>
  <li>潜在層向き施策は<strong>母数が大きい</strong>が<strong>CVRが低い</strong></li>
  <li>→ 基本は、ボトルネックを見たうえで、短期成果が必要なら顕在層、認知や将来の母数づくりが必要なら潜在層を検討します。</li>
</ul>
''', 'html.parser'))
    create_slide("参考：施策の性質", "v-model-table", mod_16)

    def mod_17(b):
        b.find('h1', class_='slide-heading').string = "集客：[PV]そもそも来てない（広告の基本）"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        main_area = b.find('main')
        if main_area:
            main_area.string = ""
            main_area.append(bs4.BeautifulSoup('''
<p style="font-size:14px; margin-bottom:16px;">「そもそも人が来てない」ときの最も直接的な打ち手 = 広告。<br>ここでのゴールは、申請書・見積書・発注仕様の中で<strong>何の目的の広告費なのか</strong>を説明できるようになることです。</p>
<h2 style="font-size:15px; color:var(--accent); margin-bottom:8px;">配信面（どこに出すか）：代表的な3つの性質を押さえる</h2>
<table class="data-table" style="font-size: 11px; margin-bottom: 20px;">
  <thead>
    <tr><th>配信面</th><th>性質</th><th>顧客の状態</th><th>向いている場面</th></tr>
  </thead>
  <tbody>
    <tr><td>検索広告</td><td>需要の回収</td><td>顕在層（今探してる）</td><td>「リフォーム 広島」で検索してる人に出す</td></tr>
    <tr><td>ディスプレイ/動画</td><td>認知・リターゲ</td><td>潜在層（まだ気づいてない）</td><td>他サイト閲覧中に目に入れる / 一度来た人に再表示</td></tr>
    <tr><td>SNS広告</td><td>ターゲット配信</td><td>中間（興味はあるかも）</td><td>年齢・趣味・行動でセグメントして届ける</td></tr>
  </tbody>
</table>
<p style="font-size:13px; margin-bottom:12px;">申請・発注に落とすときは、次の粒度まで分解できればよい：</p>
<ul class="split-list" style="font-size:13px;">
  <li><strong>どこに出すか</strong>：検索広告 / ディスプレイ広告 / SNS広告などの広告宣伝費</li>
  <li><strong>何を成果とするか</strong>：問い合わせ、資料請求、予約、購入などのCV定義</li>
  <li><strong>どこへ誘導するか</strong>：LP制作・サイト改修・商品ページ改善などの受け皿</li>
  <li><strong>どう検証するか</strong>：GA4・タグ設定・月次レポートなどの測定設計</li>
</ul>
''', 'html.parser'))
    create_slide("集客：広告の基本", "v-list", mod_17)

    def mod_18(b):
        b.find('h1', class_='slide-heading').string = "各広告の特徴とポイント"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        main_area = b.find('main')
        if main_area:
            main_area.string = ""
            main_area.append(bs4.BeautifulSoup('''
<div style="display:flex; flex-direction:column; gap:16px;">
  <article class="card" style="padding:16px;">
    <h3 style="color:var(--accent); font-size:15px; margin-bottom:8px;">🔍 検索広告：今すぐ客を刈り取る</h3>
    <ul style="font-size:12px; padding-left:20px; line-height:1.5;">
      <li>検索＝悩み。最も購買意欲が高い層（顕在層）に直接アプローチできる。</li>
      <li>Googleビジネスプロフィールと連携するだけで、<strong>地図（Googleマップ）にも同時に広告が出せる</strong>。別々に入力・予算化する必要はないため、地域密着型ビジネスには必須。</li>
    </ul>
  </article>
  
  <article class="card" style="padding:16px;">
    <h3 style="color:var(--accent); font-size:15px; margin-bottom:8px;">🖼️ ディスプレイ広告：潜在層へのリーチと追従（リタゲ）</h3>
    <ul style="font-size:12px; padding-left:20px; line-height:1.5;">
      <li>まだ検索していない「潜在層」へ広くアプローチし、認知を広げる。</li>
      <li><strong>リタゲの注意点</strong>：「過去30日で100リスト以上」など一定アクセスがないと配信されない。</li>
      <li><strong>見積りのチェック</strong>：現在は画像とテキストを自動で組み合わせる「レスポンシブ広告」が主流。全サイズ手作りで無駄な制作費が乗ってないか要確認。</li>
    </ul>
  </article>
  
  <article class="card" style="padding:16px;">
    <h3 style="color:var(--accent); font-size:15px; margin-bottom:8px;">📱 SNS広告：強力なターゲティング</h3>
    <ul style="font-size:12px; padding-left:20px; line-height:1.5;">
      <li>年齢・趣味・役職などで細かく狙い撃ちできるのが最大の強み。</li>
      <li>BtoB（法人向け）なら役職・業種で絞れるFacebook。</li>
      <li>BtoC（個人向け・視覚重視）なら写真で直感的に訴求できるInstagram。</li>
    </ul>
  </article>
</div>
''', 'html.parser'))
    create_slide("各広告の特徴とポイント", "v-list", mod_18)

    def mod_19(b):
        b.find('h1', class_='slide-heading').string = "理解・信頼：受け皿が「その人」に合っていないサイン"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        main_area = b.find('main')
        if main_area:
            main_area.string = ""
            main_area.append(bs4.BeautifulSoup('''
<p style="font-size:14px; margin-bottom:16px;">「来てるのに離脱する」のはなぜか？ 原因の一つに<strong>「受け皿が合っていない（ペルソナ不在）」</strong>があります。<br>以下の「3つのサイン」が出ていれば、それは明らかなズレの証拠です。</p>

<article class="card" style="padding:20px; border-left:4px solid var(--signal); margin-bottom:16px;">
  <h3 style="font-size:15px; font-weight:700; margin-bottom:8px;">1. 数字に出るサイン（定量のサイン）</h3>
  <ul style="font-size:13px; line-height:1.5; padding-left:20px;">
    <li>直帰率が異常に高い / 滞在時間が極端に短い（＝開いた瞬間に「違う」と判断されている）</li>
    <li>広告のクリックは多いのにCVがゼロ（＝広告の期待値とLPの内容がズレている）</li>
    <li>Google広告の「品質スコア」が低いものばかり。</li>
  </ul>
</article>

<article class="card" style="padding:20px; border-left:4px solid var(--signal); margin-bottom:16px;">
  <h3 style="font-size:15px; font-weight:700; margin-bottom:8px;">2. ファーストビュー（FV）のサイン</h3>
  <ul style="font-size:13px; line-height:1.5; padding-left:20px;">
    <li>ユーザーが検索したキーワードの「答え」が、画面のFV（最初の画面のパッと見のエリア）にない。</li>
    <li>例：「安い 引越し」で検索したのに、FVが「創業50年の信頼と実績」になっている。</li>
  </ul>
</article>

<article class="card" style="padding:20px; border-left:4px solid var(--signal);">
  <h3 style="font-size:15px; font-weight:700; margin-bottom:8px;">3. 言葉のサイン（定性のサイン）</h3>
  <ul style="font-size:13px; line-height:1.5; padding-left:20px;">
    <li>「地域No.1」「すべてのお客様に」「高品質なサービス」など、<strong>誰にでも言えるフワッとした言葉</strong>になっている。</li>
    <li>＝「誰に」がボヤけているため、結果として誰にも刺さっていない。</li>
  </ul>
</article>
''', 'html.parser'))
    create_slide("受け皿が合っていないサイン", "v-list", mod_19)

    def mod_20(b):
        b.find('h1', class_='slide-heading').string = "顧客仮説（ペルソナとカスタマージャーニー）"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        # 既存のスライド16がベース
        # 内容はほぼ同じなので流用
    create_slide("顧客仮説", "v-grid", mod_20)

    def mod_21(b):
        b.find('h1', class_='slide-heading').string = "競合仮説とコミュニケーション設計"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        # v-compare の良い事例だけ残す
        bad = b.find('article', class_='compare-card')
        if bad: bad.decompose()
        # GOODを大きく
        good = b.find('article', class_='compare-card is-selected')
        if good: good['style'] = "width: 100%;"
        
        main_area = b.find('main')
        desc = main_area.find('div', style=re.compile('grid-column: 1 / -1'))
        if desc:
            desc.replace_with(bs4.BeautifulSoup('''
<div style="grid-column: 1 / -1; padding: 12px 18px; background: #fff; border-radius: 8px; border: 1px solid var(--line); font-size: 13px; color: var(--ink);">
  <ul style="padding-left: 20px; line-height: 1.6; margin: 0;">
    <li>競合サイトを見て、「ユーザーが期待している文脈」と「自社が違いを出せる場所」を確認する。</li>
    <li>サービス内容自体での差別化が難しい場合でも、<strong>コミュニケーション（トーン・写真・言葉）で差をつける</strong>ことはできる。</li>
    <li>「万人受け」を狙うのではなく、設定したペルソナに対して自社がどう映るべきかを設計する。</li>
  </ul>
</div>
''', 'html.parser'))
        if good:
            title = good.find('h2')
            if title: title.string = "事例：エアコンクリーニング（コミュニケーションで差をつける）"
            content = good.find('div', style=re.compile('padding-top: 14px'))
            if content:
                content.replace_with(bs4.BeautifulSoup('''
<div style="padding-top: 14px; font-size: 12.5px; color: var(--ink); line-height: 1.6;">
  <p style="margin-bottom: 8px;"><strong>背景:</strong> サービス内容は本質的に同じ。機能面での差別化は不可能。</p>
  <ul class="split-list" style="margin-bottom: 8px; gap: 6px;">
    <li style="font-size: 12px;"><span class="icon-symbol" style="color: var(--ok);">check</span><span>A社「若くておしゃれなイメージ」→ 若年層・女性の一人暮らしに刺さる</span></li>
    <li style="font-size: 12px;"><span class="icon-symbol" style="color: var(--ok);">check</span><span>B社「優しくて誠実そうな雰囲気」→ ファミリー層・年配層に安心感</span></li>
  </ul>
  <p style="color: var(--ok); font-weight: 700;">結果: サイトの作りや言葉選びがまったく違い、異なるペルソナにそれぞれ響く。</p>
</div>
''', 'html.parser'))
            footer = good.find('div', style=re.compile('border-top: 1px dashed'))
            if footer:
                footer.string = "教訓：サービスで差別化できなくても、コミュニケーション（トーン・表現）で差はつけられる"
    create_slide("競合仮説とコミュニケーション設計", "v-compare", mod_21)

    def mod_22(b):
        b.find('h1', class_='slide-heading').string = "ユーザーの不安を消すためのコンテンツ・チェックリスト"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<p style="font-size:12px; margin-bottom:12px;">ここでも「絶対の正解」を作るのではなく、<strong>「ユーザーが離脱する言い訳（不安要素）」を一つずつ潰す</strong>というスタンスでサイトを確認します。<br>※「とりあえず載せるだけ」は逆効果なので、<strong>「本当に不安を消せているか（質）」</strong>までセットで確認します。</p>
<table class="data-table" style="font-size: 10px;">
  <thead>
    <tr><th>確認項目</th><th>消去したい不安</th><th>❌ ただ載せるだけ</th><th>⭕️ 質の高い載せ方</th></tr>
  </thead>
  <tbody>
    <tr><td>料金・費用感</td><td>高すぎないか？追加請求されないか？</td><td>「詳細はお問い合わせください」</td><td>目安となる金額や、追加費用の有無が明記されている</td></tr>
    <tr><td>導入事例・実績</td><td>自分の悩みが本当に解決できるのか？</td><td>「〇〇社様に導入いただきました」</td><td>「導入前はこんな最悪な状況だったが、こう解決した」というストーリーがある</td></tr>
    <tr><td>提供の流れ</td><td>しつこく営業されないか？</td><td>「お問い合わせ→面談→ご契約」</td><td>「相談だけでもOK」「手ぶらでOK」など、行動ハードルを壊している</td></tr>
    <tr><td>FAQ</td><td>迷って手が止まる心理的ハードル</td><td>「営業時間は？」「いくら？」</td><td>「他社で断られたケースでも平気？」などリアルな疑問に答えている</td></tr>
    <tr><td>保証・お約束</td><td>失敗して損をしたらどうしよう</td><td>（記載なし）</td><td>「無理な営業はしません」「全額返金保証」などの宣言がある</td></tr>
    <tr><td>第三者の評価</td><td>自称してるだけで本当は素人では？</td><td>「地域No.1（根拠なし）」</td><td>Google口コミ、メディア掲載、保有資格などが載っている</td></tr>
    <tr><td>会社・スタッフ</td><td>誰がやってるの？騙されないか？</td><td>フリー素材の笑顔の男女</td><td>代表の顔写真やメッセージ、店舗のリアルな雰囲気がわかる</td></tr>
  </tbody>
</table>
''', 'html.parser'))
    create_slide("コンテンツ・チェックリスト", "v-model-table", mod_22)

    def mod_23(b):
        b.find('h1', class_='slide-heading').string = "[コラム] 競合設定とコミュニケーション戦略"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        good = b.find('article', class_='compare-card is-selected')
        if good: good.decompose()
        bad = b.find('article', class_='compare-card')
        if bad: bad['style'] = "width: 100%;"
        
        main_area = b.find('main')
        desc = main_area.find('div', style=re.compile('grid-column: 1 / -1'))
        if desc:
            desc.replace_with(bs4.BeautifulSoup('''
<div style="grid-column: 1 / -1; padding: 12px 18px; background: #fff; border-radius: 8px; border: 1px solid var(--line); font-size: 13px; color: var(--ink);">
  <ul style="padding-left: 20px; line-height: 1.6; margin: 0;">
    <li>本編では「コミュニケーションで差をつける」成功例を見た。</li>
    <li>ただし、競合と違いを出すときは、<strong>業界や商圏の文脈から外れすぎない</strong>ことも重要。</li>
  </ul>
</div>
''', 'html.parser'))
        
        if bad:
            title = bad.find('h2')
            if title: title.string = "事例：整体院（違いすぎてダメのケース）"
            content = bad.find('div', style=re.compile('padding-top: 14px'))
            if content:
                content.replace_with(bs4.BeautifulSoup('''
<div style="padding-top: 14px; font-size: 12.5px; color: var(--ink); line-height: 1.6;">
  <p style="margin-bottom: 8px;"><strong>背景:</strong> 整体院業界は「こんなお悩みありませんか？→根本から解決！」のテンプレ構成が大多数。<br>業界コンサルが同じテンプレートを販売し、Webでの競合が同質化しすぎて均質環境が完成していた。</p>
  <p style="margin-bottom: 8px;"><strong>施策:</strong> そこに1院だけ「スタイリッシュなデザイン」で差別化を試みた。</p>
  <p style="color: var(--signal); font-weight: 700;">結果: ユーザーが期待する「整体院っぽさ」から外れすぎて、逆にCVRが上がらなかった。</p>
</div>
''', 'html.parser'))
            footer = bad.find('div', style=re.compile('border-top: 1px dashed'))
            if footer:
                footer.string = "教訓：業界、商圏のWeb上の文脈を無視した差別化は逆効果になりうる"
    create_slide("[コラム] 競合設定とコミュニケーション戦略", "v-compare", mod_23)

    def mod_24(b):
        b.find('h1', class_='slide-heading').string = "行動：[CVR] あと一歩の背中を押す（CVR改善）"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        main = b.find('main')
        if main:
            main.string = ""
            main.append(bs4.BeautifulSoup('''
<p style="font-size:14px; margin-bottom:16px;">ペルソナが合っていても、<strong>サイトの機能・導線が不親切だと離脱します。</strong><br>行動面のボトルネックに対しては、以下の施策（＝発注物）があります：</p>
<table class="data-table" style="font-size: 12px; margin-bottom: 24px;">
  <thead>
    <tr><th>施策（発注物）</th><th>内容</th><th>補助科目</th></tr>
  </thead>
  <tbody>
    <tr><td>サイト改修（EFO・CTA等）</td><td>フォーム最適化、CTA改善、電話導線、スマホ対応を発注</td><td>イ. サイト構築費</td></tr>
    <tr><td>リターゲティング広告</td><td>一度来て離脱した人に再接触する広告</td><td>オ. 広告宣伝費</td></tr>
    <tr><td>チャットボット・LINE連携等</td><td>問い合わせのハードルを下げるツール導入</td><td>イ. サイト構築費</td></tr>
  </tbody>
</table>
<div style="background:var(--ok-soft); padding:16px; border-radius:8px;">
  <h3 style="font-size:14px; color:var(--ok); font-weight:700; margin-bottom:8px;">サイト改修の発注仕様に含めるべき観点（チェックリスト）</h3>
  <ul style="font-size:12px; padding-left:20px; line-height:1.6;">
    <li><strong>フォーム</strong>：項目が多すぎないか？ スマホで入力しやすいか？（EFO）</li>
    <li><strong>CTA（行動喚起）</strong>：ボタンが目立たない / 何をすればいいか分からない状態になっていないか？</li>
    <li><strong>電話導線</strong>：スマホからワンタップで電話できるか？ 電話番号が画像になっていないか？</li>
    <li><strong>ページ速度</strong>：表示に3秒以上かかっていないか？（特にスマホ）</li>
    <li><strong>スマホ対応</strong>：PC版のレイアウトをそのまま縮小していないか？</li>
  </ul>
</div>
''', 'html.parser'))
    create_slide("CVR改善：背中を押す", "v-list", mod_24)

    def mod_25(b):
        b.find('h1', class_='slide-heading').string = "Ch2のまとめ：施策を整理する"
        b.find('span', class_='section-badge').string = "CHAPTER 02"
        p = b.find('div', class_='summary-points')
        if p:
            p.replace_with(bs4.BeautifulSoup('''
<p style="font-size:14px; margin-bottom:12px;">施策後に成果が出ないときの点検は、確認しやすい実装面から潰し、その後にペルソナ・集客へ戻ると整理しやすいです。</p>
<div style="display:flex; flex-direction:column; gap:12px;">
  <div class="card" style="padding:12px;">
    <strong>① ボトルネックと施策が一致しているかを見る</strong>
    <p style="font-size:12px; margin-top:4px; color:var(--muted)">集客不足なら流入施策、理解不足なら受け皿改善、行動詰まりなら実装改善</p>
  </div>
  <div class="card" style="padding:12px;">
    <strong>② 実装面の抜けを潰す</strong>
    <p style="font-size:12px; margin-top:4px; color:var(--muted)">フォーム、CTA、電話導線などを確認。「問題ない箇所」を消去法で潰す</p>
  </div>
  <div class="card" style="padding:12px;">
    <strong>③ ペルソナ面 → 集客の質の順で見直す</strong>
    <p style="font-size:12px; margin-top:4px; color:var(--muted)">受け皿が"その人"に合っているか？正しい人を連れてきているか？</p>
  </div>
  <div class="card" style="padding:12px;">
    <strong>④ 期待値そのものを調整する</strong>
    <p style="font-size:12px; margin-top:4px; color:var(--muted)">全部やって問題ないなら「この数字は妥当です」と伝えることも立派な支援</p>
  </div>
</div>
''', 'html.parser'))
    create_slide("Ch2まとめ", "v-summary", mod_25)

    # --- Ch3 ---
    def mod_26(b):
        b.find('div', class_='chapter-number').string = "03"
        b.find('h1', class_='chapter-title').string = "Ch3：測れるようにする"
        b.find('p', class_='chapter-body').string = "GA4を入れるだけでは、支援判断に使える数字にはなりません。\n「何を成果とするか」「途中のどこを見るか」「どこから来た人を見るか」を決めるのが測定設計です。"
    create_slide("Ch3扉", "v-chapter", mod_26)

    def mod_27(b):
        b.find('h1', class_='slide-heading').string = "やりっぱなしにしないための測定設計"
        b.find('span', class_='section-badge').string = "CHAPTER 03"
        main = b.find('main')
        if main:
            main.string = ""
            main.append(bs4.BeautifulSoup('''
<p style="font-size:16px; margin-bottom:16px;">測定設計は、GA4の操作方法を覚えることではありません。<br>毎月どの数字を見て、次の判断につなげるかを決めることです。</p>
<div class="card" style="padding:20px; border-left:4px solid var(--accent)">
  <h2 style="font-size:16px; font-weight:700; margin-bottom:12px; color:var(--accent);">最低限決めるべき4つのこと</h2>
  <ul style="font-size:14px; line-height:1.8; padding-left:24px;">
    <li><strong>最終CV</strong>：問い合わせ、購入、予約、応募など、何が増えたら成功か</li>
    <li><strong>マイクロCV</strong>：最終CVの手前にある重要な行動（フォーム到達など）</li>
    <li><strong>流入元</strong>：自然検索、広告、SNS、紹介など、どこから来た人か</li>
    <li><strong>比較単位</strong>：月次、施策前後、チャネル別など、どう比較するか</li>
  </ul>
</div>
''', 'html.parser'))
    create_slide("やりっぱなしにしない測定設計", "v-list", mod_27)

    def mod_28(b):
        b.find('h1', class_='slide-heading').string = "最終CVだけでは原因が分からない"
        b.find('span', class_='section-badge').string = "CHAPTER 03"
        # マイクロCV (既存15番流用) 
        pass
    create_slide("最終CVだけでは原因が分からない", "v-slide", mod_28)

    def mod_29(b):
        b.find('h1', class_='slide-heading').string = "月次で見る表を決める"
        b.find('span', class_='section-badge').string = "CHAPTER 03"
        main = b.find('main')
        if main:
            main.string = ""
            main.append(bs4.BeautifulSoup('''
<p style="font-size:14px; margin-bottom:16px;">Ch1で見たように、全体の数字だけでは課題を見誤ります。<br>流入元別に分けて、毎月同じ指標を見ることで、「どの施策が効いているか」「どこで止まっているか」を追いやすくなります。</p>
<ul class="split-list" style="font-size:14px; line-height:1.8;">
  <li><span class="icon-symbol" style="color:var(--accent)">check</span>全体CVRだけでなく、自然検索 / 広告 / SNS / 紹介などに分けて見る</li>
  <li><span class="icon-symbol" style="color:var(--accent)">check</span>毎月見る指標を固定する</li>
  <li><span class="icon-symbol" style="color:var(--accent)">check</span>施策前後で比較できるように、実施施策と気づきも残す</li>
</ul>
<div style="margin-top:20px; padding:16px; background:rgba(0,0,0,0.03); border-radius:8px;">
  <p style="font-size:12px; color:var(--muted)">※詳細なモニタリングシート例は別紙にて提供します。</p>
</div>
''', 'html.parser'))
    create_slide("月次で見る表を決める", "v-list", mod_29)

    def mod_30(b):
        b.find('div', class_='chapter-number').string = ""
        b.find('h1', class_='chapter-title').string = "演習 + まとめ"
        b.find('p', class_='chapter-body').string = "架空企業に対して整理の型を使い、本日の内容を定着させます。"
    create_slide("演習 + まとめ扉", "v-chapter", mod_30)

    def mod_31(b):
        b.find('h1', class_='slide-heading').string = "ケース演習とまとめ"
        b.find('span', class_='section-badge').string = "SUMMARY"
        main = b.find('main')
        if main:
            main.string = ""
            main.append(bs4.BeautifulSoup('''
<div style="display:flex; gap:24px;">
  <article class="card" style="flex:1; padding:20px;">
    <h3 style="color:var(--accent); font-weight:700; margin-bottom:12px;">ケース演習</h3>
    <ol style="font-size:13px; line-height:1.8; padding-left:20px;">
      <li>成果モデルはどれ？</li>
      <li>ボトルネックはどこ？</li>
      <li>施策は何を優先する？</li>
    </ol>
  </article>
  
  <article class="card" style="flex:1; padding:20px; border:2px solid var(--ok)">
    <h3 style="color:var(--ok); font-weight:700; margin-bottom:12px;">まとめ：迷ったらこの順番に戻る</h3>
    <div style="font-size:16px; font-weight:700; text-align:center; padding:16px; background:var(--ok-soft); border-radius:8px;">
      成果モデル<br>↓<br>ボトルネック<br>↓<br>施策<br>↓<br>測定設計
    </div>
  </article>
</div>
''', 'html.parser'))
    create_slide("演習とまとめ", "v-list", mod_31)

    def mod_32(b):
        b.find('div', class_='chapter-number').string = "A"
        b.find('h1', class_='chapter-title').string = "APPENDIX"
        b.find('p', class_='chapter-body').string = "モデル別の月間目標例や、より詳細な測定設計のチートシートです。"
    create_slide("APPENDIX扉", "v-chapter", mod_32)

    def mod_33(b):
        b.find('h1', class_='slide-heading').string = "MELSAチートシート"
        b.find('span', class_='section-badge').string = "APPENDIX"
        # 既存APPENDIX流用
    create_slide("MELSAチートシート", "v-model-table", mod_33)

    def mod_34(b):
        b.find('h1', class_='slide-heading').string = "リードモデルの月間目標例（工務店リフォーム）"
        b.find('span', class_='section-badge').string = "APPENDIX"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<div style="font-size:11px; margin-bottom:8px;"><strong>事業全体の課題</strong>：昨年はCV17件、CPA8,235円。チャネルが2つしかなくリスク分散できていない。今期はCV目標27件に引き上げつつ、CPAを改善したい。</div>
<table class="data-table" style="font-size: 9px;">
  <thead>
    <tr><th>チャネル</th><th>リーチ</th><th>訪問者</th><th>CV</th><th>CVR</th><th>月間予算</th><th>CPA</th></tr>
  </thead>
  <tbody>
    <tr><td>オーガニック</td><td>-</td><td>300</td><td>3</td><td>1.0%</td><td>0円</td><td>-</td></tr>
    <tr><td>リスティング</td><td>2,000</td><td>100</td><td>5</td><td>5.0%</td><td>5万円</td><td>10,000円</td></tr>
    <tr><td>SNS広告</td><td>8,000</td><td>40</td><td>4</td><td>10.0%</td><td>3万円</td><td>7,500円</td></tr>
    <tr><td>パートナー</td><td>5,000</td><td>60</td><td>8</td><td>13.3%</td><td>2万円</td><td>2,500円</td></tr>
    <tr><td>折込チラシ</td><td>10,000枚</td><td>15</td><td>5</td><td>0.05%</td><td>4万円</td><td>8,000円</td></tr>
    <tr style="background:#f3f4f6; font-weight:700;"><td>全体</td><td>-</td><td>525</td><td>27</td><td>-</td><td>17万円</td><td>6,296円</td></tr>
  </tbody>
</table>
''', 'html.parser'))
    create_slide("リード月間目標例", "v-model-table", mod_34)

    def mod_35(b):
        b.find('h1', class_='slide-heading').string = "ECモデルの月間目標例（アロマ販売事業者）"
        b.find('span', class_='section-badge').string = "APPENDIX"
        table = b.find('table')
        if table:
            table.replace_with(bs4.BeautifulSoup('''
<div style="font-size:11px; margin-bottom:8px;"><strong>事業全体の課題</strong>：月間売上目標150万円に対し、現状は楽天依存。自社サイト比率を上げたい。</div>
<table class="data-table" style="font-size: 9px;">
  <thead>
    <tr><th>チャネル</th><th>ユーザー</th><th>一覧</th><th>詳細</th><th>カート</th><th>CV(購入)</th><th>CVR</th><th>CPA</th></tr>
  </thead>
  <tbody>
    <tr><td>自社オーガニック</td><td>3,000</td><td>450</td><td>90</td><td>20</td><td>5</td><td>25.0%</td><td>-</td></tr>
    <tr><td>自社ネット広告</td><td>1,500</td><td>375</td><td>90</td><td>22</td><td>8</td><td>36.4%</td><td>10,000円</td></tr>
    <tr><td>SNS経由</td><td>5,000</td><td>200</td><td>30</td><td>5</td><td>1</td><td>20.0%</td><td>10,000円</td></tr>
    <tr><td>楽天</td><td>20,000</td><td>6,000</td><td>1,200</td><td>250</td><td>120</td><td>48.0%</td><td>1,000円</td></tr>
    <tr style="background:#f3f4f6; font-weight:700;"><td>全体</td><td>29,800</td><td>7,025</td><td>1,410</td><td>337</td><td>149</td><td>-</td><td>2,752円</td></tr>
  </tbody>
</table>
''', 'html.parser'))
    create_slide("EC月間目標例", "v-model-table", mod_35)

    with open('itc_tutorial_slides_new.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"完了！合計 {page_counter-1} ページ生成したよ！")

if __name__ == "__main__":
    main()
