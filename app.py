import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from deep_translator import GoogleTranslator
from langdetect import detect

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
        lang = detect(user_text)
        
        if lang == 'th':
            translated = GoogleTranslator(source='th', target='ru').translate(user_text)
            reply_text = translated
            
        elif lang == 'ru':
            translated = GoogleTranslator(source='ru', target='th').translate(user_text)
            reply_text = translated
            
        else:
            reply_text = "กรุณาส่งข้อความภาษาไทยหรือรัสเซียครับ"
            
    except Exception as e:
        reply_text = "ขออภัยครับ ไม่สามารถแปลข้อความนี้ได้"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
    
