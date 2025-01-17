from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

def handle_text_message(event):
    text = event.message.text
    
    # 基本的回覆邏輯
    if text == "打卡":
        reply_text = "收到打卡請求！"
    elif text == "查詢":
        reply_text = "這是你的出勤紀錄"
    else:
        reply_text = f"你說了：{text}"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
