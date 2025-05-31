import os
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from dotenv import load_dotenv
import json
import base64

app = Flask(__name__)
load_dotenv()

# Google Sheets API認証情報
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_random_delay():
    """ランダムな遅延を生成"""
    return random.uniform(2, 5)

def get_hakoniwa_products(category=None, max_pages=1):
    products = []
    ua = UserAgent()
    base_url = 'https://www.hakoniwear.com'
    
    # カテゴリーページのURLを生成
    if category:
        url = f'{base_url}/category/{category}'
    else:
        url = f'{base_url}/products'
    
    try:
        # ランダムなユーザーエージェントを使用
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.find_all('div', class_='product-item')
            
            for item in items:
                try:
                    # 商品情報の抽出
                    title_elem = item.find('h3', class_='product-title')
                    price_elem = item.find('span', class_='price')
                    image_elem = item.find('img')
                    link_elem = item.find('a')
                    
                    if title_elem and price_elem:
                        # 在庫状況の確認
                        stock_status = '在庫あり'
                        if item.find('span', class_='sold-out'):
                            stock_status = '在庫なし'
                        
                        product = {
                            'title': title_elem.text.strip(),
                            'price': price_elem.text.strip().replace('¥', '').replace(',', ''),
                            'image_url': image_elem.get('src', '') if image_elem else '',
                            'product_url': base_url + link_elem.get('href', '') if link_elem else '',
                            'availability': stock_status
                        }
                        products.append(product)
                except Exception as e:
                    print(f"商品情報の抽出エラー: {str(e)}")
                    continue
            
            # 遅延を入れる
            time.sleep(get_random_delay())
        else:
            print(f"ページの取得に失敗: {response.status_code}")
            
    except Exception as e:
        print(f"処理中にエラー: {str(e)}")
    
    return products

def get_credentials_json():
    """環境変数からcredentials.jsonを取得"""
    credentials_base64 = os.getenv('GOOGLE_CREDENTIALS_BASE64')
    if credentials_base64:
        credentials_json = base64.b64decode(credentials_base64).decode('utf-8')
        return json.loads(credentials_json)
    return None

def get_google_sheets_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_json = get_credentials_json()
            if credentials_json:
                flow = InstalledAppFlow.from_client_config(
                    credentials_json, SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            else:
                raise Exception("Google認証情報が見つかりません")

    return build('sheets', 'v4', credentials=creds)

def update_spreadsheet(products):
    service = get_google_sheets_service()
    
    # データの準備
    values = []
    for product in products:
        values.append([
            product.get('title', ''),
            product.get('price', ''),
            product.get('availability', ''),
            product.get('image_url', ''),
            product.get('product_url', '')
        ])
    
    body = {
        'values': values
    }
    
    # スプレッドシートの更新
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A2',  # ヘッダー行の下から開始
        valueInputOption='RAW',
        body=body
    ).execute()

@app.route('/', methods=['GET'])
def index():
    return 'Hakoniwa Spreadsheet API is running.'

@app.route('/update', methods=['POST'])
def update_data():
    try:
        # 各カテゴリーの商品を取得
        categories = ['kids', 'baby', 'adult']
        all_products = []
        
        for category in categories:
            products = get_hakoniwa_products(category=category)
            all_products.extend(products)
        
        update_spreadsheet(all_products)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 