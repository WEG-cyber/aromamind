import os
import pandas as pd
import random
import google.generativeai as genai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage, ButtonsTemplate, URITemplateAction,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, TextSendMessage, ButtonComponent
)

app = Flask(__name__)

# --- 設定 LINE Channel 資訊 ---
LINE_CHANNEL_ACCESS_TOKEN = 'et9QpJnYAZureB5+wajvigSUbUJZ989aasP/vWn5O0ijAe3roZZ3ptcy7QaYSGCKVL+cwmBLJSHS2gHNqxMRIGogZ31tdRQ61NMRn8yMVrZU8nhw2ibkExvev2rq/B0XCk+LpCzEWBMdFzxgXvzztgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'a8fb1a6810912ad9110a700e5a758272'
GOOGLE_API_KEY = 'AIzaSyDz18zQV20BvoYzg1MSJjbMckFmNFKz1wQ'
LIFF_URL = 'https://liff.line.me/2009990334-b3WXj4PN'
# 預設背景圖 (使用您之前生成的禪風圖)
DEFAULT_IMAGE_URL = 'https://weg-cyber.github.io/aromamind/line-square-1040.png'

# 設定 Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 載入精油資料
try:
    oils_df = pd.read_csv('all_essential_oils.csv')
except Exception as e:
    oils_df = None

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/broadcast", methods=['GET'])
def broadcast():
    try:
        if oils_df is not None:
            row = oils_df.sample().iloc[0]
            name_en = row['name_en']
            name_zh = row.get('name_zh', name_en) # 如果有中文名就用，沒有就用英文
            desc = row['description_summary']
            
            # 建立 Flex Message 圖卡
            flex_message = create_oil_flex_card(name_zh, name_en, desc)
            line_bot_api.broadcast(flex_message)
            return "Broadcast success!", 200
        return "No data to broadcast", 404
    except Exception as e:
        return f"Broadcast failed: {e}", 500

@app.route("/remind_breathing", methods=['GET'])
def remind_breathing():
    try:
        message = TextSendMessage(text="🌬️ 下午三點了，休息一下吧！\n\n放下手邊的工作，花三分鐘跟著 AromaMind 進行一次深呼吸訓練，幫大腦重新開機。")
        line_bot_api.broadcast(message)
        return "Reminder success!", 200
    except Exception as e:
        return f"Reminder failed: {e}", 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    system_prompt = f"你是一位專業且溫暖的芳療師，名字叫 'AromaMind AI'。語氣親切有禪意。最後請鼓勵使用者開啟 AromaMind 網頁進行深呼吸。網址是 {LIFF_URL}。"
    try:
        response = model.generate_content(f"{system_prompt}\n\n使用者說：{user_text}")
        ai_reply = response.text.strip()
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=ai_reply),
                TemplateSendMessage(
                    alt_text='開啟 AromaMind 指南',
                    template=ButtonsTemplate(
                        title='AromaMind 芳療建議',
                        text='您可以開啟指南查看詳細按摩手法',
                        actions=[URITemplateAction(label='開啟深呼吸與指南', uri=LIFF_URL)]
                    )
                )
            ]
        )
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，我的大腦正在冥想中，請稍後再試！"))

def create_oil_flex_card(name_zh, name_en, desc):
    bubble = BubbleContainer(
        hero=ImageComponent(
            url=DEFAULT_IMAGE_URL,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text="🌿 今日精油推薦", weight='bold', color='#1DB446', size='sm'),
                TextComponent(text=name_zh, weight='bold', size='xl', margin='md'),
                TextComponent(text=name_en, size='xs', color='#aaaaaa', font_style='italic'),
                BoxComponent(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(text=desc, wrap=True, color='#666666', size='sm', flex=5)
                            ]
                        )
                    ]
                )
            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='primary',
                    height='sm',
                    color='#8FB1A5',
                    action=URITemplateAction(label='開啟 AromaMind 指南', uri=LIFF_URL)
                )
            ]
        )
    )
    return FlexSendMessage(alt_text=f"今日精油推薦：{name_zh}", contents=bubble)

if __name__ == "__main__":
    app.run(port=5000)
