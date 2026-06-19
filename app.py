@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    
    try:
        # ตรวจสอบว่าเป็นภาษาอะไร
        lang = detect(user_text)
        
        if lang == 'th':
            # ถ้าเป็นภาษาไทย ให้แปลเป็นรัสเซีย
            translated = GoogleTranslator(source='th', target='ru').translate(user_text)
            reply_text = translated
            
        elif lang == 'ru':
            # ถ้าเป็นภาษารัสเซีย ให้แปลเป็นไทย
            translated = GoogleTranslator(source='ru', target='th').translate(user_text)
            reply_text = translated
            
        else:
            # ถ้าเป็นภาษาอื่นๆ (เช่น อังกฤษ) ให้แจ้งเตือน
            reply_text = "กรุณาส่งข้อความภาษาไทยหรือรัสเซียครับ"
            
    except Exception as e:
        # กรณีตรวจจับภาษาไม่ได้ (เช่น ส่งสติ๊กเกอร์ หรือพิมพ์อีโมจิมาอย่างเดียว)
        reply_text = "ขออภัยครับ ไม่สามารถแปลข้อความนี้ได้"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
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
    
