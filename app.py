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

SITE_OILS = [
    {
        "id": "lavender",
        "name_zh": "薰衣草",
        "name_en": "Lavender oil",
        "description": "最廣為人知的精油，具有強大的鎮靜與舒緩力量。它是芳療界的萬用油。",
        "use_categories": "舒緩壓力、改善睡眠、緩解頭痛、修復皮膚",
        "safety": "低血壓者使用過量可能導致倦怠，請少量使用。",
    },
    {
        "id": "peppermint",
        "name_zh": "歐薄荷",
        "name_en": "Peppermint oil",
        "description": "清涼清爽的香氣，能瞬間提神醒腦，並緩解各種身體不適。",
        "use_categories": "提升專注力、緩解鼻塞、減輕噁心、清涼止癢",
        "safety": "避開眼睛周圍；嬰幼兒、孕婦與蠶豆症患者應避免使用。",
    },
    {
        "id": "eucalyptus",
        "name_zh": "尤加利",
        "name_en": "Eucalyptus oil",
        "description": "具有強勁穿透力，是呼吸道的守護者，能淨化空氣並激發活力。",
        "use_categories": "淨化呼吸道、提升免疫力、清空思緒、環境除臭",
        "safety": "不宜口服；幼童與敏感族群使用前請先諮詢專業人士。",
    },
    {
        "id": "tea_tree",
        "name_zh": "茶樹",
        "name_en": "Tea tree oil",
        "description": "強效的天然防護劑，具有清新的木質香氣，是居家必備的淨化之星。",
        "use_categories": "天然抑菌、平衡油脂、提升防護力、調理肌膚",
        "safety": "不可口服；氧化後的精油可能導致皮膚過敏。",
    },
    {
        "id": "bergamot",
        "name_zh": "佛手柑",
        "name_en": "Bergamot oil",
        "description": "兼具柑橘清新與花香優雅，是快樂精油，能同時提振與安撫情緒。",
        "use_categories": "緩解焦慮、提振精神、支持消化、放鬆心情",
        "safety": "具有光敏性，塗抹於皮膚後 12 小時內避免日曬。",
    },
    {
        "id": "frankincense",
        "name_zh": "乳香",
        "name_en": "Frankincense oil",
        "description": "神聖且深沉的木質香調，能讓呼吸變慢變深，帶領心靈進入平靜。",
        "use_categories": "深層放鬆、平撫情緒、抗老修護、加深呼吸",
        "safety": "孕期使用請諮詢專業意見。",
    },
    {
        "id": "clary_sage",
        "name_zh": "快樂鼠尾草",
        "name_en": "Clary Sage oil",
        "description": "溫暖、帶點堅果味的草本香，是女性的好隊友，能舒緩週期不適。",
        "use_categories": "平衡情緒、放鬆肌肉、女性週期支持、幫助入夢",
        "safety": "懷孕期間禁用；使用後避免飲酒。",
    },
    {
        "id": "sweet_orange",
        "name_zh": "甜橙",
        "name_en": "Orange oil",
        "description": "溫暖陽光的香氣，像寒冬中的擁抱，能帶來純粹的喜悅感。",
        "use_categories": "驅散低落、緩解壓力、幫助入睡、改善食慾",
        "safety": "具輕微光敏性，皮膚使用後請留意日曬。",
    },
    {
        "id": "rosemary",
        "name_zh": "迷迭香",
        "name_en": "Rosemary oil",
        "description": "強勁的草本香氣，被稱為記憶之草，能激發大腦活力。",
        "use_categories": "增強記憶、提高專注力、促進循環、緩解肌肉痠痛",
        "safety": "高血壓與癲癇患者應避免使用；懷孕期間不建議使用。",
    },
]

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

def build_oil_url(oil):
    return f"{SITE_URL}?oil={oil['id']}&openExternalBrowser=1"

def create_oil_info_card(oil):
    """
    仿照截圖中的「訂房紀錄」卡片格式，
    直接在 LINE 裡顯示精油的完整資料。
    """
    name_zh = str(oil.get('name_zh', '今日精油'))
    name_en = str(oil.get('name_en', 'Essential oil'))
    oil_type = str(oil.get('oil_type', '芳療精油'))
    botanical = str(oil.get('botanical_names', ''))
    desc = str(oil.get('description', ''))
    use_cat = str(oil.get('use_categories', ''))
    safety = str(oil.get('safety', ''))
    image_url = get_plant_image(name_en)
    oil_url = build_oil_url(oil)

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
                },
                {
                    "type": "text",
                    "text": name_zh,
                    "size": "lg",
                    "weight": "bold",
                    "color": "#6d8c8e",
                    "margin": "xs"
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
                        "label": f"查看{name_zh}完整頁面",
                        "uri": oil_url
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
        alt_text=f"🌿 今日精油推薦：{name_zh}（{name_en}）",
        contents=flex_body
    )

@app.route("/broadcast", methods=['GET'])
def broadcast():
    try:
        oil = random.choice(SITE_OILS)
        flex_message = create_oil_info_card(oil)
        line_bot_api.broadcast(flex_message)
        return f"Broadcast success! Oil: {oil['name_zh']} ({oil['id']})", 200
    except Exception as e:
        import traceback
        return f"Broadcast failed: {e}\n{traceback.format_exc()}", 500

@app.route("/remind_breathing", methods=['GET'])
def remind_breathing():
    try:
        breathing_url = f"{SITE_URL}?openExternalBrowser=1"
        message = TextSendMessage(
            text=(
                "🌬️ 下午三點了，起來動一動吧！\n\n"
                "離開椅子、伸展肩頸，再花三分鐘跟著 AromaMind 做一次深呼吸。\n"
                f"{breathing_url}"
            )
        )
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
    3. 只推薦網站支援的精油：薰衣草 lavender、歐薄荷 peppermint、尤加利 eucalyptus、茶樹 tea_tree、佛手柑 bergamot、乳香 frankincense、快樂鼠尾草 clary_sage、甜橙 sweet_orange、迷迭香 rosemary。
    4. 連結格式為: {SITE_URL}?oil=[精油ID]&openExternalBrowser=1
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
