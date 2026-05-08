import os
import pandas as pd
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction

app = Flask(__name__)

# --- 設定 LINE Channel 資訊 (請將以下替換為您的資訊) ---
LINE_CHANNEL_ACCESS_TOKEN = 'et9QpJnYAZureB5+wajvigSUbUJZ989aasP/vWn5O0ijAe3roZZ3ptcy7QaYSGCKVL+cwmBLJSHS2gHNqxMRIGogZ31tdRQ61NMRn8yMVrZU8nhw2ibkExvev2rq/B0XCk+LpCzEWBMdFzxgXvzztgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'a8fb1a6810912ad9110a700e5a758272'
LIFF_URL = 'https://liff.line.me/2009990334-b3WXj4PN'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 載入精油資料
try:
    oils_df = pd.read_csv('all_essential_oils.csv')
    blends_df = pd.read_csv('compound_massage_oil_blends.csv')
except Exception as e:
    print(f"Error loading CSV files: {e}")
    oils_df = None
    blends_df = None

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
    # 這是觸發定時發送的通道
    try:
        oil_tip = get_random_oil_tip()
        message = TextSendMessage(text=f"☀️ 早安！今天的芳療小知識來了：\n\n{oil_tip}")
        line_bot_api.broadcast(message)
        return "Broadcast success!", 200
    except Exception as e:
        return f"Broadcast failed: {e}", 500


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()
    
    # 簡易對話邏輯
    if "你好" in user_text or "hello" in user_text:
        reply = "你好！我是您的 AromaMind 芳療師。請問今天有什麼我可以幫您的嗎？您可以輸入症狀（如：頭痛、壓力）來獲取建議。"
    
    elif "頭痛" in user_text or "緊繃" in user_text:
        reply = "針對頭痛，我推薦您使用『歐薄荷』或『薰衣草』。您可以點擊下方按鈕開啟指南，查看具體的按摩練習。"
        send_liff_button(event, reply)
        return

    elif "壓力" in user_text or "焦慮" in user_text:
        reply = "感到壓力嗎？試試看『佛手柑』或『乳香』。現在就開啟指南，跟著圓圈做三分鐘的深呼吸吧。"
        send_liff_button(event, reply)
        return

    elif "知識" in user_text or "推薦" in user_text:
        oil_tip = get_random_oil_tip()
        reply = f"【今日精油小知識】\n\n{oil_tip}"
    
    else:
        reply = f"我收到了您的訊息：'{user_text}'。想尋找適合的精油嗎？您可以直接開啟我們的 AromaMind 指南：\n{LIFF_URL}"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

def send_liff_button(event, text):
    buttons_template = TemplateSendMessage(
        alt_text='開啟 AromaMind 指南',
        template=ButtonsTemplate(
            title='AromaMind 芳療師建議',
            text=text,
            actions=[
                URITemplateAction(
                    label='開啟深呼吸與指南',
                    uri=LIFF_URL
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)

def get_random_oil_tip():
    if oils_df is not None:
        row = oils_df.sample().iloc[0]
        name = row['name_en']
        desc = row['description_summary']
        return f"🌟 精油名稱：{name}\n\n💡 簡介：{desc}\n\n希望這個知識對您有幫助！"
    return "今天暫時沒有精油小知識，記得深呼吸哦！"

if __name__ == "__main__":
    app.run(port=5000)
