import re

with open('/Users/yukimichihata/seminar計画/itc_tutorial_slides.html', 'r', encoding='utf-8') as f:
    content = f.read()

# チャンクの抽出 (2198行目から2571行目に相当する部分)
start_marker = "  <!-- ============================================================\n     SLIDE 11 / CV構造と計測の基本\n     ============================================================ -->"
end_marker = "  <!-- ============================================================\n     APPENDIX TITLE / 扉\n     ============================================================ -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found!")
    exit(1)

new_slides = """  <!-- ============================================================
     SLIDE 11 / 成果までの道のりを「フロー図」で描く
     ============================================================ -->
  <div class="template-block">
    <div class="label">11 / 成果までの道のりを「フロー図」で描く</div>
    <section class="slide v-funnel" aria-label="成果までの道のりをフロー図で描く">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">2つ目の問い：「どこで止まっているか？」</h1>
      </header>
      <main class="content-area">
        <div style="grid-column: 1 / -1; margin-bottom: -10px; color: var(--ink); font-size: 13px; font-weight: 700;">
          ユーザーは一直線に成果（CV）には至りません。「どこで止まっているか」を知るために、ステップを分解します。
        </div>
        
        <!-- ECモデル -->
        <article class="card funnel-card" style="padding: 16px;">
          <div class="eyebrow" style="color: var(--accent);">ECモデルの例</div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div style="flex:1; text-align:center; padding:10px; background:rgba(53,36,138,0.08); border-radius:4px; font-size:12px; font-weight:700;">ランディング</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(53,36,138,0.08); border-radius:4px; font-size:12px; font-weight:700;">カテゴリ</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(53,36,138,0.08); border-radius:4px; font-size:12px; font-weight:700;">商品詳細</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(53,36,138,0.08); border-radius:4px; font-size:12px; font-weight:700;">カート</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(53,36,138,0.08); border-radius:4px; font-size:12px; font-weight:700;">情報入力</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:var(--ok-soft); border:1px solid var(--ok); border-radius:4px; font-size:12px; font-weight:700; color:var(--ok);">決済完了</div>
          </div>
        </article>

        <!-- リードジェネレーションモデル -->
        <article class="card funnel-card" style="padding: 16px;">
          <div class="eyebrow" style="color: var(--ok);">リード獲得モデルの例</div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div style="flex:1; text-align:center; padding:10px; background:rgba(21,99,86,0.08); border-radius:4px; font-size:12px; font-weight:700;">広告/検索</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(21,99,86,0.08); border-radius:4px; font-size:12px; font-weight:700;">LP/記事</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(21,99,86,0.08); border-radius:4px; font-size:12px; font-weight:700;">フォーム到達</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(21,99,86,0.08); border-radius:4px; font-size:12px; font-weight:700;">入力完了</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(21,99,86,0.08); border-radius:4px; font-size:12px; font-weight:700;">商談</div>
            <span class="icon-symbol" style="color:var(--muted); font-size:16px;">arrow_forward</span>
            <div style="flex:1; text-align:center; padding:10px; background:var(--ok-soft); border:1px solid var(--ok); border-radius:4px; font-size:12px; font-weight:700; color:var(--ok);">受注</div>
          </div>
        </article>
      </main>
      <footer class="slide-footer">
        <div class="conclusion">
          <span class="icon-symbol" aria-label="要点">analytics</span>
          <p class="conc-text">最終成果に至るまでのステップを可視化することで、「どこで止まっているか」が初めて議論できます。</p>
        </div>
        <span class="page-num">11 / 25</span>
      </footer>
    </section>
  </div>

  <!-- ============================================================
     SLIDE 12 / フローの「詰まり」とWebの4つの打ち手
     ============================================================ -->
  <div class="template-block">
    <div class="label">12 / フローの「詰まり」とWebの4つの打ち手</div>
    <section class="slide v-grid" aria-label="フローの詰まりと打ち手">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">「課題特定」×「Webの打ち手」がリンクする</h1>
      </header>
      <main class="content-area">
        <article class="card" style="padding: 16px;">
          <h2 class="item-title" style="color: var(--accent); display:flex; align-items:center; gap:6px;">
            <span class="icon-symbol">group_add</span> ① 入り口が少ない ＝「集客」
          </h2>
          <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">症状：LP到達が少ない、知られていない</p>
          <div style="background:rgba(53,36,138,0.05); padding:10px; border-radius:4px; font-size:12px;">
            <strong>打ち手：</strong>広告配信、SEO対策、SNS運用
          </div>
        </article>

        <article class="card" style="padding: 16px;">
          <h2 class="item-title" style="color: var(--ok); display:flex; align-items:center; gap:6px;">
            <span class="icon-symbol">support_agent</span> ② 中間で離脱する ＝「接客」
          </h2>
          <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">症状：一覧から詳細に行かない、LPからフォームに行かない</p>
          <div style="background:var(--ok-soft); padding:10px; border-radius:4px; font-size:12px;">
            <strong>打ち手：</strong>LP改善、コンテンツ強化、導入事例の追加
          </div>
        </article>

        <article class="card" style="padding: 16px;">
          <h2 class="item-title" style="color: var(--signal); display:flex; align-items:center; gap:6px;">
            <span class="icon-symbol">shopping_cart_checkout</span> ③ 直前で離脱する ＝「追客」
          </h2>
          <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">症状：カート投入後に買わない、フォーム入力中に離脱</p>
          <div style="background:var(--signal-soft); padding:10px; border-radius:4px; font-size:12px;">
            <strong>打ち手：</strong>EFO（入力フォーム最適化）、リターゲティング広告
          </div>
        </article>

        <article class="card" style="padding: 16px;">
          <h2 class="item-title" style="color: #4f5068; display:flex; align-items:center; gap:6px;">
            <span class="icon-symbol">query_stats</span> ④ 全体が見えない ＝「測定」
          </h2>
          <p style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">症状：どこで止まっているかの数字自体が取れていない</p>
          <div style="background:#f3f4f6; padding:10px; border-radius:4px; font-size:12px;">
            <strong>打ち手：</strong>GA4設計、コンバージョンタグの設定
          </div>
        </article>
      </main>
      <footer class="slide-footer">
        <div class="conclusion">
          <span class="icon-symbol" aria-label="要点">tips_and_updates</span>
          <p class="conc-text">フローの「どこで止まっているか」が特定できれば、Webマーケの「4つの打ち手」が論理的に決まります。</p>
        </div>
        <span class="page-num">12 / 25</span>
      </footer>
    </section>
  </div>

  <!-- ============================================================
     SLIDE 13 / 成果モデル別の課題分解
     ============================================================ -->
  <div class="template-block">
    <div class="label">13 / 成果モデル別の課題分解</div>
    <section class="slide v-model-table" aria-label="成果モデル別の課題分解">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">「分解すると、どこが悪いかが見える」を体感する</h1>
      </header>
      <main class="content-area" style="grid-template-rows: auto auto; gap: 12px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; height: 100%;">
          <!-- ECモデル -->
          <div class="card" style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
            <div class="eyebrow" style="color: var(--accent);">ECモデルの例</div>
            <div style="overflow-x: auto; flex: 1;">
              <table id="ec-model-table" class="data-table" style="font-size: 10.5px;">
                <thead>
                  <tr>
                    <th style="padding: 6px;">指標</th>
                    <th style="padding: 6px;">モールA</th>
                    <th style="padding: 6px;">フリマB</th>
                    <th style="padding: 6px;">自社店舗</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6px;">全ユーザー</td>
                    <td style="padding: 6px;">40,000</td>
                    <td style="padding: 6px;">30,000</td>
                    <td style="padding: 6px;">6,000</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px;">商品一覧到達率</td>
                    <td style="padding: 6px; color: var(--signal); font-weight: 700;">7.5%</td>
                    <td style="padding: 6px;">50.0%</td>
                    <td style="padding: 6px;">50.0%</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px;">商品詳細到達率</td>
                    <td style="padding: 6px;">10.0%</td>
                    <td style="padding: 6px; color: var(--signal); font-weight: 700;">2.0%</td>
                    <td style="padding: 6px;">10.0%</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px;">CVR(カート→購入)</td>
                    <td style="padding: 6px;">20.0%</td>
                    <td style="padding: 6px;">20.0%</td>
                    <td style="padding: 6px;">20.0%</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              style="background: var(--signal-soft); padding: 10px; border-radius: 6px; font-size: 11.5px; color: var(--ink);">
              <span class="icon-symbol"
                style="font-size: 14px; color: var(--signal); vertical-align: middle;">arrow_forward</span>
              <strong>モールA</strong>：一覧到達率が極端に低い（集客の質の問題）<br>
              <span class="icon-symbol"
                style="font-size: 14px; color: var(--signal); vertical-align: middle;">arrow_forward</span>
              <strong>フリマB</strong>：詳細到達率が低い（一覧→詳細の導線問題）
            </div>
          </div>

          <!-- リード獲得モデル -->
          <div class="card" style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
            <div class="eyebrow" style="color: var(--ok);">リード獲得モデルの例</div>
            <div style="overflow-x: auto; flex: 1;">
              <table id="lead-model-table" class="data-table" style="font-size: 10.5px;">
                <thead>
                  <tr>
                    <th
                      style="padding: 6px; background: linear-gradient(180deg, rgba(21, 99, 86, 0.94), rgba(21, 99, 86, 0.86));">
                      指標</th>
                    <th style="padding: 6px;">マッチングA</th>
                    <th style="padding: 6px;">パートナーB</th>
                    <th style="padding: 6px;">自社サイト</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6px; background: rgba(21, 99, 86, 0.065);">訪問率</td>
                    <td style="padding: 6px; color: var(--signal); font-weight: 700;">6.25%</td>
                    <td style="padding: 6px;">25.0%</td>
                    <td style="padding: 6px;">25.0%</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px; background: rgba(21, 99, 86, 0.065);">CVR</td>
                    <td style="padding: 6px; font-weight: 700; color: var(--ok);">20.0%</td>
                    <td style="padding: 6px; color: var(--signal); font-weight: 700;">4.0%</td>
                    <td style="padding: 6px;">20.0%</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px; background: rgba(21, 99, 86, 0.065);">商談率</td>
                    <td style="padding: 6px;">20.0%</td>
                    <td style="padding: 6px; font-weight: 700; color: var(--ok);">40.0%</td>
                    <td style="padding: 6px;">20.0%</td>
                  </tr>
                  <tr>
                    <td style="padding: 6px; background: rgba(21, 99, 86, 0.065);">受注率</td>
                    <td style="padding: 6px;">25.0%</td>
                    <td style="padding: 6px; font-weight: 700; color: var(--ok);">50.0%</td>
                    <td style="padding: 6px;">25.0%</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              style="background: rgba(21, 99, 86, 0.08); padding: 10px; border-radius: 6px; font-size: 11.5px; color: var(--ink);">
              <span class="icon-symbol"
                style="font-size: 14px; color: var(--ok); vertical-align: middle;">arrow_forward</span>
              <strong>マッチングA</strong>：訪問率は低いが、CVRは優秀（流入の質に課題）<br>
              <span class="icon-symbol"
                style="font-size: 14px; color: var(--ok); vertical-align: middle;">arrow_forward</span>
              <strong>パートナーB</strong>：CVRは低いが、商談化率が優秀（サイトの受け皿に課題）
            </div>
          </div>
        </div>
      </main>
      <footer class="slide-footer">
        <div class="conclusion is-ok">
          <span class="icon-symbol" aria-label="要点">insights</span>
          <p class="conc-text">「数字を分解すると、感覚ではなく根拠で課題を特定できる。」これはITCが得意な領域そのものです。</p>
        </div>
        <span class="page-num">13 / 25</span>
      </footer>
    </section>
  </div>

  <!-- ============================================================
     SLIDE 14 / 計測の落とし穴とマイクロCV
     ============================================================ -->
  <div class="template-block">
    <div class="label">14 / 計測の落とし穴とマイクロCV</div>
    <section class="slide v-notes" aria-label="計測の落とし穴とマイクロCV">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">計測とマイクロCV：少ないデータを改善根拠に変える</h1>
      </header>
      <main class="content-area">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height:100%;">
          
          <!-- GA4の話 -->
          <article class="card note-card" style="border: 1px solid var(--signal);">
            <div class="eyebrow" style="color: var(--signal);">WARNING</div>
            <h2 class="item-title">GA4は「入れただけ」では測れない</h2>
            <p class="body-text" style="margin-top: 8px;">
              「問い合わせ完了」や「電話タップ」などの重要な行動は、手動でイベントの設計（タグ・トリガ設定）をしないと計測されません。
            </p>
            <div style="margin-top: auto; padding: 12px; background: var(--signal-soft); border-radius: 6px; font-weight: 700; color: var(--ink); font-size: 12.5px;">
              <span class="icon-symbol" style="color: var(--signal); vertical-align: middle; margin-right: 4px;">contact_support</span>
              現場で必ず聞くこと<br>
              <span style="font-weight: normal; margin-top: 4px; display: block;">🗣️「重要な行動は、イベントとして計測・コンバージョン指定されていますか？」</span>
            </div>
          </article>

          <!-- マイクロCVの話 -->
          <article class="card note-card" style="border: 1px solid var(--ok);">
            <div class="eyebrow" style="color: var(--ok);">MICRO CV</div>
            <h2 class="item-title">最終CVの手前にある中間行動</h2>
            <p class="body-text" style="margin-top: 8px;">
              月に数件しか問い合わせがない中小企業では、最終CVだけではブレが大きすぎて改善根拠が作れません。
            </p>
            <ul class="split-list" style="margin-top: auto;">
              <li><span class="icon-symbol">ads_click</span><span>フォーム到達・入力開始</span></li>
              <li><span class="icon-symbol">call</span><span>電話番号タップ</span></li>
              <li><span class="icon-symbol">menu_book</span><span>導入事例・料金ページの閲覧</span></li>
            </ul>
          </article>

        </div>
      </main>
      <footer class="slide-footer">
        <div class="conclusion">
          <span class="icon-symbol" aria-label="要点">troubleshoot</span>
          <p class="conc-text">計測設計とマイクロCVは、「最終CVが少ない」状況でも分析を可能にする道具です。</p>
        </div>
        <span class="page-num">14 / 25</span>
      </footer>
    </section>
  </div>

  <!-- ============================================================
     SLIDE 15 / 顧客仮説 — ペルソナとジャーニー
     ============================================================ -->
  <div class="template-block">
    <div class="label">15 / 顧客仮説 — ペルソナとジャーニー</div>
    <section class="slide v-grid" aria-label="顧客仮説">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">3つ目の問い：「誰からその成果を得るのか？」</h1>
      </header>
      <main class="content-area">
        <div class="lead-text" style="grid-column: 1 / -1; margin-bottom: 0;">
          <span class="icon-symbol">person_search</span>
          <p class="lead-content">
            ペルソナは「細かい人物像」ではなく、<strong>「状況・不安・選定基準を揃える道具」</strong>です。
          </p>
        </div>

        <article class="card" style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
          <h2 class="item-title" style="color: var(--accent); font-size: 14px;">現場で確認すべき顧客の解像度</h2>
          <ul class="split-list">
            <li><span class="icon-symbol">person</span><span><strong>顧客の状況</strong>：今、どんな困りごとを抱えているか？</span></li>
            <li><span class="icon-symbol">psychology</span><span><strong>不安</strong>：依頼する前に、どんなことを心配しているか？</span></li>
            <li><span class="icon-symbol">rule</span><span><strong>選定基準</strong>：他社と迷ったとき、何が決め手になるか？</span></li>
            <li><span class="icon-symbol">search</span><span><strong>検索行動</strong>：どんなキーワードで探し始めるか？</span></li>
          </ul>
        </article>

        <article class="card"
          style="padding: 16px; display: flex; flex-direction: column; gap: 12px; border: 2px solid var(--ok);">
          <h2 class="item-title" style="color: var(--ok); font-size: 14px;">競合設定と差別化のリアル</h2>
          <div
            style="background: var(--ok-soft); padding: 12px; border-radius: 6px; font-size: 12px; color: var(--ink);">
            <p style="margin-bottom: 8px;">🗣️「競合と比べてどこで選ばれていますか？」を必ず聞きます。</p>
            <ul style="padding-left: 20px; color: var(--muted); line-height: 1.5;">
              <li>明確な差別化（価格・品質・立地等）があれば訴求軸へ。</li>
              <li><strong>現実には「明確に差別化できない」ケースのほうが多い。</strong></li>
              <li>→ その場合、<strong>コミュニケーション（サイトのトーン・表現・写真・言葉選び）で差をつける</strong>ことが重要になります。</li>
            </ul>
          </div>
        </article>
      </main>
      <footer class="slide-footer">
        <div class="conclusion">
          <span class="icon-symbol" aria-label="要点">design_services</span>
          <p class="conc-text">「誰に届けるか」と「競合とどう差をつけるか」が決まると、広告・サイト・トーンのグランドデザインが決まります。</p>
        </div>
        <span class="page-num">15 / 25</span>
      </footer>
    </section>
  </div>

  <!-- ============================================================
     SLIDE 16 / 競合設定とコミュニケーション戦略
     ============================================================ -->
  <div class="template-block">
    <div class="label">16 / 競合設定とコミュニケーション戦略</div>
    <section class="slide v-compare" aria-label="競合設定とコミュニケーション戦略">
      <div class="top-bar"></div>
      <header class="slide-header">
        <span class="section-badge">CHAPTER 02</span>
        <h1 class="slide-heading">重要な原則：「同じすぎてもダメ、違いすぎてもダメ」</h1>
      </header>
      <main class="content-area">
        <div
          style="grid-column: 1 / -1; padding: 12px 18px; background: #fff; border-radius: 8px; border: 1px solid var(--line); font-size: 13px; color: var(--ink);">
          競合のサイトを見ずに施策を決めてはいけません。業界のWeb上の文脈（生態系）を理解した上で、立ち位置を決めます。
        </div>

        <article class="card compare-card">
          <div class="compare-head">
            <div>
              <div class="eyebrow" style="color: var(--signal);">BAD CASE</div>
              <h2 class="item-title">事例①：整体院（違いすぎてダメ）</h2>
            </div>
            <span class="icon-symbol" style="color: var(--signal); font-size: 28px;">sentiment_dissatisfied</span>
          </div>
          <div style="padding-top: 14px; font-size: 12.5px; color: var(--ink); line-height: 1.6;">
            <p style="margin-bottom: 8px;"><strong>背景:</strong> 業界コンサルの影響で、周りの競合が「こんなお悩みありませんか？」のテンプレ構成ばかり。</p>
            <p style="margin-bottom: 8px;"><strong>施策:</strong> 1院だけ「スタイリッシュなデザイン」で差別化を試みた。</p>
            <p style="color: var(--signal); font-weight: 700;">結果: ユーザーが期待する「整体院っぽさ」から外れすぎてCVRが上がらない。</p>
          </div>
          <div
            style="margin-top: auto; padding-top: 12px; border-top: 1px dashed var(--line); font-size: 11px; color: var(--muted); font-weight: 700;">
            教訓：業界、商圏のWeb上の文脈を無視した差別化は逆効果。
          </div>
        </article>

        <article class="card compare-card is-selected">
          <div class="compare-head">
            <div>
              <div class="eyebrow" style="color: var(--ok);">GOOD CASE</div>
              <h2 class="item-title" style="color: var(--ok);">事例②：エアコン清掃（トーンで差別化）</h2>
            </div>
            <span class="icon-symbol" style="color: var(--ok); font-size: 28px;">sentiment_satisfied</span>
          </div>
          <div style="padding-top: 14px; font-size: 12.5px; color: var(--ink); line-height: 1.6;">
            <p style="margin-bottom: 8px;"><strong>背景:</strong> サービス内容は本質的に同じ。機能面での差別化は不可能。</p>
            <ul class="split-list" style="margin-bottom: 8px; gap: 6px;">
              <li style="font-size: 12px;"><span class="icon-symbol"
                  style="color: var(--ok);">check</span><span>A社「若くておしゃれ」→ 若年層・女性に刺さる</span></li>
              <li style="font-size: 12px;"><span class="icon-symbol"
                  style="color: var(--ok);">check</span><span>B社「優しくて誠実」→ ファミリー層・年配層に安心感</span></li>
            </ul>
            <p style="color: var(--ok); font-weight: 700;">結果: 異なるペルソナにそれぞれ響き、CVが獲得できる。</p>
          </div>
          <div
            style="margin-top: auto; padding-top: 12px; border-top: 1px dashed rgba(31, 118, 103, 0.3); font-size: 11px; color: var(--ok); font-weight: 700;">
            教訓：サービスで差別化できなくても、コミュニケーションで差は作れる。
          </div>
        </article>
      </main>
      <footer class="slide-footer">
        <div class="conclusion">
          <span class="icon-symbol" aria-label="要点">balance</span>
          <p class="conc-text">競合を見て「同じすぎないか」「外れすぎないか」を確認し、差別化が難しければコミュニケーション戦略で差をつけます。</p>
        </div>
        <span class="page-num">16 / 25</span>
      </footer>
    </section>
  </div>
"""

content = content[:start_idx] + new_slides + content[end_idx:]

# 全ての / 25 を / 26 に置換する (ただしページ数表記に関わるところのみ安全に)
content = re.sub(r'(\d{2})\s*/\s*25', r'\1 / 26', content)

with open('/Users/yukimichihata/seminar計画/itc_tutorial_slides.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement successful")
