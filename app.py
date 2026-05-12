import os
import requests
import pandas as pd
import random
import json
import google.generativeai as genai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage
)

app = Flask(__name__)

# --- 設定 LINE Channel 資訊 ---
LINE_CHANNEL_ACCESS_TOKEN = 'et9QpJnYAZureB5+wajvigSUbUJZ989aasP/vWn5O0ijAe3roZZ3ptcy7QaYSGCKVL+cwmBLJSHS2gHNqxMRIGogZ31tdRQ61NMRn8yMVrZU8nhw2ibkExvev2rq/B0XCk+LpCzEWBMdFzxgXvzztgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'a8fb1a6810912ad9110a700e5a758272'
GOOGLE_API_KEY = 'AIzaSyDz18zQV20BvoYzg1MSJjbMckFmNFKz1wQ'
SITE_URL = 'https://weg-cyber.github.io/aromamind/'
DEFAULT_IMAGE_URL = 'https://weg-cyber.github.io/aromamind/line-square-1040.png'

# 設定 Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 載入精油資料
try:
    oils_df = pd.read_csv('all_essential_oils.csv')
    print(f"Loaded {len(oils_df)} oils from CSV")
except Exception as e:
    oils_df = None
    print(f"Failed to load CSV: {e}")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_plant_image(name_en):
    try:
        search_term = name_en.replace(' oil', '').replace(' Oil', '').strip().replace(' ', '_')
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'originalimage' in data:
                return data['originalimage']['source']
            elif 'thumbnail' in data:
                return data['thumbnail']['source']
    except Exception as e:
        print(f"Wikipedia image fetch failed for {name_en}: {e}")
    return DEFAULT_IMAGE_URL

def create_oil_info_card(row):
    """
    仿照截圖中的「訂房紀錄」卡片格式，
    直接在 LINE 裡顯示精油的完整資料。
    """
    name_en = str(row.get('name_en', '未知精油'))
    oil_type = str(row.get('oil_type', ''))
    botanical = str(row.get('botanical_names', ''))
    desc = str(row.get('description_summary', ''))
    use_cat = str(row.get('use_categories', ''))
    safety = str(row.get('safety_flags', ''))
    image_url = get_plant_image(name_en)

    # 截斷過長的描述 (LINE 有字數限制)
    if len(desc) > 120:
        desc = desc[:117] + '...'

    # 構建資訊列（只顯示有值的欄位）
    info_rows = []

    if botanical and botanical not in ['', 'nan']:
        info_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "🌱 學名", "size": "sm", "color": "#888888", "flex": 2},
                {"type": "text", "text": botanical, "size": "sm", "color": "#333333", "flex": 5, "wrap": True}
            ],
            "margin": "sm"
        })

    if oil_type and oil_type not in ['', 'nan']:
        info_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "🧴 類型", "size": "sm", "color": "#888888", "flex": 2},
                {"type": "text", "text": oil_type, "size": "sm", "color": "#333333", "flex": 5, "wrap": True}
            ],
            "margin": "sm"
        })

    if use_cat and use_cat not in ['', 'nan']:
        info_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "✨ 用途", "size": "sm", "color": "#888888", "flex": 2},
                {"type": "text", "text": use_cat, "size": "sm", "color": "#333333", "flex": 5, "wrap": True}
            ],
            "margin": "sm"
        })

    if safety and safety not in ['', 'nan', '0']:
        info_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "⚠️ 注意", "size": "sm", "color": "#888888", "flex": 2},
                {"type": "text", "text": safety, "size": "sm", "color": "#c0392b", "flex": 5, "wrap": True}
            ],
            "margin": "sm"
        })

    # 使用原生 dict 格式構建 Flex Message（更靈活）
    flex_body = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🌿 今日精油推薦",
                            "size": "xs",
                            "color": "#6d8c8e",
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": name_en,
                    "size": "xl",
                    "weight": "bold",
                    "color": "#1a1a1a",
                    "margin": "sm"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#ffffff"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": desc if desc and desc not in ['nan', ''] else "今日為您精選的芳療精油",
                    "size": "sm",
                    "color": "#555555",
                    "wrap": True,
                    "margin": "none"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#eeeeee"
                }
            ] + info_rows,
            "paddingAll": "15px",
            "backgroundColor": "#ffffff"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "🌐 開啟 AromaMind 網站",
                        "uri": f"{SITE_URL}?openExternalBrowser=1"
                    },
                    "style": "primary",
                    "color": "#6d8c8e",
                    "height": "sm"
                }
            ],
            "paddingAll": "12px",
            "backgroundColor": "#f8f9fa"
        }
    }

    return FlexSendMessage(
        alt_text=f"🌿 今日精油推薦：{name_en}",
        contents=flex_body
    )

@app.route("/broadcast", methods=['GET'])
def broadcast():
    try:
        if oils_df is not None:
            row = oils_df.sample().iloc[0]
            flex_message = create_oil_info_card(row)
            line_bot_api.broadcast(flex_message)
            return f"Broadcast success! Oil: {row['name_en']}", 200
        return "No data", 404
    except Exception as e:
        import traceback
        return f"Broadcast failed: {e}\n{traceback.format_exc()}", 500

@app.route("/remind_breathing", methods=['GET'])
def remind_breathing():
    try:
        message = TextSendMessage(text="🌬️ 下午三點了，休息一下吧！\n\n放下手邊的工作，花三分鐘跟著 AromaMind 進行一次深呼吸訓練。")
        line_bot_api.broadcast(message)
        return "Reminder success!", 200
    except Exception as e:
        return f"Reminder failed: {e}", 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    system_prompt = f"""
    你是一位專業芳療師 AromaMind AI。
    1. 語氣溫暖有禪意。
    2. 當你推薦特定精油時，請在最後附上專屬連結。
    3. 連結格式為: {SITE_URL}?oil=[精油英文名稱]&openExternalBrowser=1
    """
    try:
        response = model.generate_content(f"{system_prompt}\n\n使用者說：{user_text}")
        ai_reply = response.text.strip()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ai_reply)
        )
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，我的大腦正在冥想中..."))

if __name__ == "__main__":
    app.run(port=5000)
