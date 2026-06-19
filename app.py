from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from deep_translator import GoogleTranslator
from langdetect import detect
import os

app = Flask(__name__)

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
        # ตรวจสอบภาษา
        lang = detect(user_text)
        
        # ถ้าเป็นไทย (th) ให้แปลเป็นรัสเซีย (ru)
        if lang == 'th':
            translated = GoogleTranslator(source='th', target='ru').translate(user_text)
            reply_text = f"🇷🇺 แปลเป็นภาษารัสเซีย:\n{translated}"
        # ถ้าเป็นรัสเซีย (ru) ให้แปลเป็นไทย (th)
        elif lang == 'ru':
            translated = GoogleTranslator(source='ru', target='th').translate(user_text)
            reply_text = f"🇹🇭 แปลเป็นภาษาไทย:\n{translated}"
        else:
            # กรณีภาษาอื่น ให้แปลเป็นไทย
            translated = GoogleTranslator(source='auto', target='th').translate(user_text)
            reply_text = f"🇹🇭 แปลเป็นภาษาไทย:\n{translated}"
            
    except Exception as e:
        reply_text = "ขออภัยครับ เกิดข้อผิดพลาดในการแปล"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

