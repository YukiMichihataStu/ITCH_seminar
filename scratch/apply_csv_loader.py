import os

def apply_csv_loader(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. スライド10のテーブルにIDを追加
    # <table class="data-table" style="height: auto;"> を置換
    target_10 = '<table class="data-table" style="height: auto;">'
    replacement_10 = '<table id="management-issues-table" class="data-table" style="height: auto;">'
    if target_10 in content:
        content = content.replace(target_10, replacement_10, 1)
        print(f"Added #management-issues-table to {file_path}")
    
    # 2. スライド13と14のテーブルにIDを追加
    # <table class="data-table" style="font-size: 11px;">
    # 複数あるので、順番に置換
    target_table = '<table class="data-table" style="font-size: 11px;">'
    
    # まず1番目の出現 (ECモデル) を ec-model-table に置換
    if target_table in content:
        content = content.replace(target_table, '<table id="ec-model-table" class="data-table" style="font-size: 11px;">', 1)
        print(f"Added #ec-model-table to {file_path}")
        
    # 次の出現 (リードモデル) を lead-model-table に置換
    if target_table in content:
        content = content.replace(target_table, '<table id="lead-model-table" class="data-table" style="font-size: 11px;">', 1)
        print(f"Added #lead-model-table to {file_path}")

    # 3. JavaScriptの挿入
    js_code = """
  <!-- ============================================================
     CSV Dynamic Loader Script
     ============================================================ -->
  <script>
    // 📊 CSVデータ動的読み込み & レンダリングロジック
    (function() {
      const LOG_TAG = "📊[CSV-Loader]";
      const logInfo = (msg) => console.log(`[ℹ️INFO] ${LOG_TAG} ${msg}`);
      const logSuccess = (msg) => console.log(`[✅SUCCESS] ${LOG_TAG} ${msg}`);
      const logWarn = (msg) => console.warn(`[⚠️WARN] ${LOG_TAG} ${msg}`);
      const logError = (msg, err) => console.error(`[❌ERROR] ${LOG_TAG} ${msg}`, err);

      // HTML特殊文字のサニタイズ
      function escapeHtml(str) {
        if (typeof str !== 'string') return str;
        return str.replace(/[&<>'"]/g, (tag) => ({
          '&': '&amp;',
          '<': '&lt;',
          '>': '&gt;',
          "'": '&#39;',
          '"': '&quot;'
        }[tag] || tag));
      }

      // 簡易CSVパーサー（ダブルクォーテーション対応）
      function parseCSV(text) {
        const lines = [];
        let row = [""];
        let inQuotes = false;

        for (let i = 0; i < text.length; i++) {
          const c = text[i];
          const next = text[i+1];
          if (c === '"') {
            if (inQuotes && next === '"') {
              row[row.length - 1] += '"';
              i++;
            } else {
              inQuotes = !inQuotes;
            }
          } else if (c === ',' && !inQuotes) {
            row.push("");
          } else if ((c === '\\r' || c === '\\n') && !inQuotes) {
            if (c === '\\r' && next === '\\n') {
              i++;
            }
            lines.push(row);
            row = [""];
          } else {
            row[row.length - 1] += c;
          }
        }
        if (row.length > 1 || row[0] !== "") {
          lines.push(row);
        }
        return lines;
      }

      // 経営課題と成果モデルの紐付けテーブル（スライド10）のレンダリング
      function renderManagementIssues(table, data) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        
        // ヘッダー行をスキップ
        for (let i = 1; i < data.length; i++) {
          const row = data[i];
          if (row.length < 5) continue;
          const [model, issue, cv, kpi_title, kpi_desc] = row;
          
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td style="padding-top: 14px; padding-bottom: 14px;">
              <span class="tag" style="font-size: 10px; padding: 2px 8px; background: var(--signal-soft); color: var(--signal); display: inline-block; margin-bottom: 6px;">${escapeHtml(model)}</span>
              <div style="font-weight: 700;">${escapeHtml(issue)}</div>
            </td>
            <td style="vertical-align: middle; font-weight: 700;">${escapeHtml(cv)}</td>
            <td style="vertical-align: middle; font-size: 11px; line-height: 1.5; color: var(--ink);">
              <div style="font-weight: 700; color: var(--accent); margin-bottom: 4px;">${escapeHtml(kpi_title)}</div>
              <div style="color: var(--muted);">${escapeHtml(kpi_desc)}</div>
            </td>
          `;
          tbody.appendChild(tr);
        }
      }

      // 数値テーブル（スライド13, 14）の更新
      function updateBreakdownTable(table, data) {
        const rows = table.querySelectorAll('tbody tr');
        
        for (let i = 1; i < data.length; i++) {
          const csvRow = data[i];
          if (csvRow.length <= 1) continue;
          
          const metricName = csvRow[0].trim();
          let targetRow = null;
          
          // 1列目の指標名でマッチングする行を探す
          for (const tr of rows) {
            const firstTd = tr.querySelector('td');
            if (firstTd && firstTd.textContent.includes(metricName)) {
              targetRow = tr;
              break;
            }
          }
          
          if (targetRow) {
            const tds = targetRow.querySelectorAll('td');
            for (let j = 1; j < csvRow.length; j++) {
              if (tds[j]) {
                let val = csvRow[j].trim();
                let isSignal = false;
                let isOk = false;
                
                // 強調マークの処理
                if (val.endsWith('*')) {
                  val = val.slice(0, -1);
                  isSignal = true;
                } else if (val.endsWith('!')) {
                  val = val.slice(0, -1);
                  isOk = true;
                }
                
                tds[j].textContent = val;
                
                // スタイルのリセットと再設定
                tds[j].style.color = '';
                tds[j].style.fontWeight = '';
                
                if (isSignal) {
                  tds[j].style.color = 'var(--signal)';
                  tds[j].style.fontWeight = '700';
                } else if (isOk) {
                  tds[j].style.color = 'var(--ok)';
                  tds[j].style.fontWeight = '700';
                }
              }
            }
          }
        }
      }

      // CSV読み込みメイン処理
      async function loadTable(url, tableId, renderer) {
        logInfo(`Loading CSV from: ${url}`);
        try {
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          const text = await response.text();
          const data = parseCSV(text);
          
          const table = document.getElementById(tableId);
          if (!table) {
            throw new Error(`Table #${tableId} not found`);
          }
          
          renderer(table, data);
          logSuccess(`Table #${tableId} successfully updated from CSV.`);
        } catch (err) {
          logWarn(`Failed to load ${url} for #${tableId}. Using offline fallback static HTML.`);
          logError(err.message, err);
        }
      }

      // DOM読み込み完了後に実行
      document.addEventListener("DOMContentLoaded", () => {
        loadTable('data/management_issues.csv', 'management-issues-table', renderManagementIssues);
        loadTable('data/ec_model_breakdown.csv', 'ec-model-table', updateBreakdownTable);
        loadTable('data/lead_model_breakdown.csv', 'lead-model-table', updateBreakdownTable);
      });
    })();
  </script>
"""
    
    # </body> の直前に挿入
    if '</body>' in content:
        # 既にスクリプトが入っているかチェック
        if 'CSV Dynamic Loader Script' not in content:
            content = content.replace('</body>', js_code + '\n</body>')
            print(f"Embedded JavaScript loader in {file_path}")
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# HTMLファイルに適用
apply_csv_loader('/Users/yukimichihata/seminar計画/itc_tutorial_slides.template.html')
apply_csv_loader('/Users/yukimichihata/seminar計画/itc_tutorial_slides.html')

# replace_slides.py にもIDを追加する
replace_py_path = '/Users/yukimichihata/seminar計画/replace_slides.py'
if os.path.exists(replace_py_path):
    with open(replace_py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()
        
    # ECモデルのテーブルにIDを追加
    py_content = py_content.replace(
        '<table class="data-table" style="font-size: 10.5px;">',
        '<table id="ec-model-table" class="data-table" style="font-size: 10.5px;">',
        1
    )
    # リード獲得モデルのテーブルにIDを追加
    py_content = py_content.replace(
        '<table class="data-table" style="font-size: 10.5px;">',
        '<table id="lead-model-table" class="data-table" style="font-size: 10.5px;">',
        1
    )
    with open(replace_py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)
    print("Updated table IDs in replace_slides.py")
