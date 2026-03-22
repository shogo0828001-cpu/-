"""メルカリ転売利益計算アプリ"""

import csv
import io
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List

from profit_calculator import ProfitCalculator
from amazon_api import AmazonAPI

app = FastAPI(title="メルカリ転売利益計算")
amazon = AmazonAPI()

# シンプルなHTMLインターフェース
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>メルカリ転売利益計算</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        .upload-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input[type="file"], input[type="number"] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
            font-size: 14px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .results {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        thead {
            background: #f5f5f5;
        }
        th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #ddd;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f9f9f9;
        }
        .profit-positive {
            color: #10b981;
            font-weight: 600;
        }
        .profit-negative {
            color: #ef4444;
            font-weight: 600;
        }
        .message {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .message.info {
            background: #e0f2fe;
            color: #0369a1;
        }
        .message.error {
            background: #fee2e2;
            color: #b91c1c;
        }
        .message.success {
            background: #dcfce7;
            color: #166534;
        }
        .loading {
            display: none;
            text-align: center;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 メルカリ転売利益計算</h1>
            <p class="subtitle">Amazon仕入れ価格とメルカリ売却価格から自動で利益を計算</p>
        </header>

        <div class="upload-section">
            <h2>ステップ 1: データをアップロード</h2>
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="csvFile">メルカリ商品情報（CSVファイル）</label>
                    <input type="file" id="csvFile" name="file" accept=".csv" required>
                    <small style="color: #666; margin-top: 5px; display: block;">
                        ※CSV形式: 商品名, メルカリ想定売却価格 (例: iPhone 13, 50000)
                    </small>
                </div>

                <div class="form-group">
                    <label for="shippingCost">送料（円）デフォルト: 500</label>
                    <input type="number" id="shippingCost" name="shipping_cost" value="500" min="0">
                </div>

                <button type="submit">計算開始</button>
            </form>
        </div>

        <div id="loading" class="loading">
            <p>計算中...</p>
        </div>

        <div id="resultsContainer"></div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData();
            const file = document.getElementById('csvFile').files[0];
            const shippingCost = document.getElementById('shippingCost').value;

            if (!file) {
                alert('CSVファイルを選択してください');
                return;
            }

            formData.append('file', file);
            formData.append('shipping_cost', shippingCost);

            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultsContainer').innerHTML = '';

            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                displayResults(data);
            } catch (error) {
                displayError('エラーが発生しました: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });

        function displayResults(data) {
            const container = document.getElementById('resultsContainer');

            if (data.error) {
                displayError(data.error);
                return;
            }

            const results = data.results || [];
            const profitable = results.filter(r => r.is_profitable);

            let html = '<div class="results">';
            html += `<h2>📈 計算結果</h2>`;
            html += `<div class="message info">合計 ${results.length} 件 / 利益が出る商品 ${profitable.length} 件</div>`;

            if (results.length === 0) {
                html += '<div class="message error">データを読み込めませんでした</div>';
            } else {
                html += '<table>';
                html += '<thead><tr>';
                html += '<th>商品名</th>';
                html += '<th>メルカリ売却価格</th>';
                html += '<th>Amazon仕入れ価格</th>';
                html += '<th>手数料</th>';
                html += '<th>送料</th>';
                html += '<th>利益</th>';
                html += '<th>利益率</th>';
                html += '</tr></thead><tbody>';

                results.forEach(item => {
                    const profitClass = item.profit > 0 ? 'profit-positive' : 'profit-negative';
                    html += '<tr>';
                    html += `<td>${escapeHtml(item.product_name)}</td>`;
                    html += `<td>¥${item.mercari_price.toLocaleString()}</td>`;
                    html += `<td>¥${item.amazon_price.toLocaleString()}</td>`;
                    html += `<td>¥${item.mercari_fee.toLocaleString()}</td>`;
                    html += `<td>¥${item.shipping_cost.toLocaleString()}</td>`;
                    html += `<td class="${profitClass}">¥${item.profit.toLocaleString()}</td>`;
                    html += `<td class="${profitClass}">${item.profit_rate}%</td>`;
                    html += '</tr>';
                });

                html += '</tbody></table>';
            }

            html += '</div>';
            container.innerHTML = html;
        }

        function displayError(message) {
            const container = document.getElementById('resultsContainer');
            container.innerHTML = `<div class="results"><div class="message error">${escapeHtml(message)}</div></div>`;
        }

        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    """トップページ"""
    return HTML_TEMPLATE

@app.post("/api/calculate")
async def calculate(file: UploadFile = File(...), shipping_cost: float = Form(500)):
    """
    CSVをアップロードして利益を計算

    Args:
        file: CSVファイル
        shipping_cost: 送料

    Returns:
        計算結果
    """
    try:
        contents = await file.read()
        csv_text = contents.decode('utf-8')

        # CSVを解析
        csv_reader = csv.reader(io.StringIO(csv_text))
        results = []

        for row_idx, row in enumerate(csv_reader):
            if row_idx == 0 or not row or len(row) < 2:
                continue  # ヘッダーか空行をスキップ

            try:
                product_name = row[0].strip()
                mercari_price = float(row[1].strip())

                # Amazon価格を取得（現在はモック）
                amazon_product = amazon.search_by_keyword(product_name)
                amazon_price = amazon_product['Price'] if amazon_product else 0

                # 利益計算
                profit_data = ProfitCalculator.calculate(
                    mercari_price=mercari_price,
                    amazon_price=amazon_price,
                    shipping_cost=shipping_cost
                )

                result = {
                    'product_name': product_name,
                    **profit_data
                }
                results.append(result)
            except (ValueError, IndexError) as e:
                # 不正な行はスキップ
                continue

        # 利益率でソート（降順）
        results.sort(key=lambda x: x['profit_rate'], reverse=True)

        return {'results': results}

    except Exception as e:
        return {'error': str(e)}, 400
