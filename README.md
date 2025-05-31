# Hakoniwa-Spreadsheet

ハコニワプロダクツ（https://www.hakoniwear.com/）の商品データを自動で取得し、Googleスプレッドシートに反映するツールです。

## 機能
- ハコニワプロダクツのWebサイトから商品データ（タイトル、価格、在庫、画像URL、商品URL）を自動取得
- 取得したデータをGoogleスプレッドシートに自動反映
- Herokuでのデプロイに対応

## セットアップ

1. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

2. Google Sheets APIの設定:
   - Google Cloud Consoleでプロジェクトを作成
   - Google Sheets APIを有効化
   - 認証情報（OAuth2.0クライアントID）を作成し、`credentials.json`をダウンロード
   - `credentials.json`をBase64エンコードし、環境変数`GOOGLE_CREDENTIALS_BASE64`に設定

3. スプレッドシートIDの取得:
   - GoogleスプレッドシートのURLからID部分をコピーし、環境変数`SPREADSHEET_ID`に設定

4. 環境変数の設定:
   - `.env`ファイル、またはHerokuの環境変数に以下を設定
```
SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials
```

## デプロイ（Heroku）

1. Herokuアプリ作成（未作成の場合）
```bash
heroku create hakoniwaapp
```

2. Herokuに環境変数を設定
```bash
heroku config:set SPREADSHEET_ID=your_spreadsheet_id -a hakoniwaapp
heroku config:set GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials -a hakoniwaapp
```

3. デプロイ
```bash
git push heroku main
```

4. Dyno（webプロセス）をONにする
```bash
heroku ps:scale web=1 -a hakoniwaapp
```

## 使用方法

1. アプリケーションを起動（ローカルの場合）:
```bash
python app.py
```

2. データ更新:
- POSTリクエストを`/update`エンドポイントに送信

## 注意事項
- 認証情報は必ず環境変数として管理してください
- Google Sheets APIの認証情報は安全に管理してください
- スクレイピング対象サイトの利用規約を遵守してください

---

GitHub: https://github.com/ai9129/Hakoniwa-Spreadsheet 