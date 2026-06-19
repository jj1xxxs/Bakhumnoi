import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from deep_translator import GoogleTranslator
from langdetect import detect

app = Flask(__name__)

# ดึง Token จาก Environment Variables ที่เราตั้งไว้ใน Railway
line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    
    try:
        # ตรวจสอบว่าเป็นภาษาไทยหรือไม่
        lang = detect(user_text)
        
        if lang == 'th':
            # แปลจากไทย (th) เป็นรัสเซีย (ru)
            translated = GoogleTranslator(source='th', target='ru').translate(user_text)
            reply_text = f"🇷🇺 แปลเป็นภาษารัสเซีย:\n{translated}"
        else:
            reply_text = "กรุณาส่งข้อความภาษาไทยครับ ผมจะแปลเป็นภาษารัสเซียให้"
            
    except Exception as e:
        reply_text = "ขออภัยครับ เกิดข้อผิดพลาดในการแปล"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
    
