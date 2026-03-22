# メルカリ転売利益計算アプリ

Amazon仕入れ → メルカリ売却の転売で、利益が出る商品を簡単に見つけられるアプリです。

## 特徴

✅ **CSVで商品情報を入力**
- メルカリ想定売却価格を入力するだけ
- Amazon仕入れ価格は自動取得（モック対応）

✅ **自動利益計算**
- メルカリ手数料（10%）を自動差引
- 送料を考慮した正確な利益を計算
- 利益率で自動ソート

✅ **見やすいUI**
- ブラウザで簡単に操作
- 一覧表で利益が出る商品を確認

## インストール

```bash
# 依存パッケージをインストール
pip install -r requirements.txt
```

## 使い方

### 1. アプリを起動

```bash
uvicorn main:app --reload
```

ブラウザで `http://localhost:8000` を開く

### 2. CSVファイルを準備

**CSV形式:**
```
商品名,メルカリ想定売却価格
iPhone 13,50000
AirPods Pro,20000
Magic Keyboard,15000
```

または `sample.csv` を使用してテスト

### 3. ファイルをアップロード

1. CSVファイルを選択
2. 送料を入力（デフォルト: 500円）
3. 「計算開始」ボタンをクリック

### 4. 結果を確認

利益が出そうな商品が利益率順に表示されます

## 利益計算ロジック

```
利益 = メルカリ売却価格 - メルカリ手数料(10%) - Amazon仕入れ価格 - 送料
利益率(%) = (利益 / Amazon仕入れ価格) × 100
```

## 今後の拡張

- [ ] Amazon Product Advertising APIと連携（自動価格取得）
- [ ] メルカリWeb APIとの連携
- [ ] 商品ごとの送料設定
- [ ] 利益率フィルター機能
- [ ] CSV出力機能
- [ ] データベース保存

## 設定方法

### Amazon APIを使用する場合

`.env` ファイルを作成：

```
AMAZON_API_KEY=your_api_key
AMAZON_API_SECRET=your_api_secret
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

## ライセンス

MIT License
