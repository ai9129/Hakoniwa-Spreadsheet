# Amazon-Spreadsheet

Amazonの商品データを取得し、Googleスプレッドシートに反映するツールです。

## 機能

- Amazon Product Advertising APIを使用して商品データを取得
- 取得したデータをGoogleスプレッドシートに自動反映
- Herokuでのデプロイに対応

## セットアップ

1. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

2. 環境変数の設定:
- `.env.example`を`.env`にコピーし、必要な認証情報を設定してください。

3. Google Sheets APIの設定:
- Google Cloud Consoleでプロジェクトを作成
- Google Sheets APIを有効化
- 認証情報をダウンロードし、`credentials.json`として保存

4. Amazon APIの設定:
- Amazon Seller Centralでアプリケーションを登録
- 必要な認証情報を取得

## デプロイ

Herokuへのデプロイ:
```bash
heroku create
git push heroku main
```

## 使用方法

1. アプリケーションを起動:
```bash
python app.py
```

2. データ更新:
- POSTリクエストを`/update`エンドポイントに送信

## 注意事項

- 認証情報は必ず環境変数として設定してください
- Google Sheets APIの認証情報は安全に管理してください
- Amazon APIの利用制限に注意してください 