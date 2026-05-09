import os
import pandas as pd
import random
import google.generativeai as genai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction

app = Flask(__name__)

# --- 設定 LINE Channel 資訊 ---
LINE_CHANNEL_ACCESS_TOKEN = 'et9QpJnYAZureB5+wajvigSUbUJZ989aasP/vWn5O0ijAe3roZZ3ptcy7QaYSGCKVL+cwmBLJSHS2gHNqxMRIGogZ31tdRQ61NMRn8yMVrZU8nhw2ibkExvev2rq/B0XCk+LpCzEWBMdFzxgXvzztgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'a8fb1a6810912ad9110a700e5a758272'
GOOGLE_API_KEY = 'AIzaSyDz18zQV20BvoYzg1MSJjbMckFmNFKz1wQ'
LIFF_URL = 'https://liff.line.me/2009990334-b3WXj4PN'

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
        oil_tip = get_random_oil_tip()
        message = TextSendMessage(text=f"☀️ 早安！今天的芳療小知識來了：\n\n{oil_tip}")
        line_bot_api.broadcast(message)
        return "Broadcast success!", 200
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
    
    # 建立系統提示詞 (System Prompt)
    system_prompt = f"""
    你是一位專業且溫暖的芳療師，名字叫 'AromaMind AI'。
    你的任務是根據使用者的情緒或身體狀況推薦精油。
    請遵循以下原則：
    1. 語氣要親切、優雅、有禪意。
    2. 如果使用者提到特定的症狀（如頭痛、失眠），請給予專業建議。
    3. 在回答的最後，請鼓勵使用者開啟 AromaMind 網頁進行深呼吸。
    4. 儘量保持簡短，適合在 LINE 上閱讀。
    """
    
    try:
        # 使用 Gemini 產生回答
        response = model.generate_content(f"{system_prompt}\n\n使用者說：{user_text}")
        ai_reply = response.text.strip()
        
        # 傳送回答
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

def get_random_oil_tip():
    if oils_df is not None:
        row = oils_df.sample().iloc[0]
        name = row['name_en']
        desc = row['description_summary']
        return f"🌟 精油名稱：{name}\n\n💡 簡介：{desc}\n\n希望這個知識對您有幫助！"
    return "今天暫時沒有精油小知識，記得深呼吸哦！"

if __name__ == "__main__":
    app.run(port=5000)
