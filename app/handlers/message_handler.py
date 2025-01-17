from linebot import LineBotApi
from linebot.models import TextSendMessage
import os
from app.services.attendance_service import AttendanceService

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

class MessageHandler:
    def __init__(self):
        self.attendance_service = AttendanceService()

    def handle_message(self, event):
        user_id = event.source.user_id
        message_text = event.message.text
        
        # 獲取用戶資料
        try:
            profile = line_bot_api.get_profile(user_id)
            user_name = profile.display_name
        except Exception as e:
            print(f"獲取用戶資料失敗: {str(e)}")
            user_name = "未知用戶"

        if message_text == "上班打卡":
            response = self.attendance_service.record_clock_in(user_id, user_name)
        elif message_text == "下班打卡":
            response = self.attendance_service.record_clock_out(user_id, user_name)
        elif message_text == "查詢打卡":
            response = self.attendance_service.get_attendance_record(user_id)
        else:
            response = "請輸入：上班打卡、下班打卡 或 查詢打卡"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

# 創建全局實例
message_handler = MessageHandler()

def handle_message(event):
    return message_handler.handle_message(event)