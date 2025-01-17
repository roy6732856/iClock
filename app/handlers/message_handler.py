from flask import request
from linebot.models import LocationMessage
import os
from app.services.attendance_service import AttendanceService
from app.services.line_service import LineService
from app.models.user import User
from app.models.company import Company
from app.utils.database import db

# 為了更好的邏輯分離，我們可以創建一個新的處理器類
class UserRegistrationHandler:
    def __init__(self, line_service):
        self.line_service = line_service

    def handle_new_user(self, event, user_id):
        profile = self.line_service.get_profile(user_id)
        user = User(line_user_id=user_id, display_name=profile.display_name)
        db.session.add(user)
        db.session.commit()
        
        self.line_service.send_text_message(
            event.reply_token,
            "歡迎使用打卡系統！請輸入您的公司代碼進行綁定。"
        )
        return user

class CompanyBindingHandler:
    def __init__(self, line_service):
        self.line_service = line_service

    def handle_company_binding(self, event, user, company_code):
        company = Company.query.filter_by(code=company_code).first()
        if company:
            user.company_id = company.id
            db.session.commit()
            self.line_service.send_text_message(
                event.reply_token,
                f"成功綁定至公司：{company.name}"
            )
            return True
        else:
            self.line_service.send_text_message(
                event.reply_token,
                "無效的公司代碼，請重新輸入。"
            )
            return False

class MessageHandler:
    pending_actions = {}

    def __init__(self):
        self.line_service = LineService(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        self.attendance_service = AttendanceService()
        self.user_registration = UserRegistrationHandler(self.line_service)
        self.company_binding = CompanyBindingHandler(self.line_service)

    def handle_message(self, event):
        user_id = event.source.user_id
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()

        user = User.query.filter_by(line_user_id=user_id).first()
        
        # 處理新用戶註冊
        if not user:
            user = self.user_registration.handle_new_user(event, user_id)
            return

        # 處理公司綁定
        if not user.company_id:
            self.company_binding.handle_company_binding(event, user, event.message.text)
            return

        # 處理位置消息
        if isinstance(event.message, LocationMessage):
            self._handle_location_message(event, user, user_id, ip_address)
            return

        # 處理文字消息
        self._handle_text_message(event, user, user_id)

    def _handle_location_message(self, event, user, user_id, ip_address):
        location = {
            'latitude': event.message.latitude,
            'longitude': event.message.longitude,
            'address': event.message.address
        }
        
        if user_id in self.pending_actions:
            action = self.pending_actions[user_id]
            response = None
            
            if action == "上班打卡":
                response = self.attendance_service.record_clock_in(
                    user_id, user.display_name, ip_address, location
                )
            elif action == "下班打卡":
                response = self.attendance_service.record_clock_out(
                    user_id, user.display_name, ip_address, location
                )
                
            if response:
                del self.pending_actions[user_id]
                self.line_service.send_text_message(event.reply_token, response)

    def _handle_text_message(self, event, user, user_id):
        message_text = event.message.text
        
        if message_text in ["上班打卡", "下班打卡"]:
            # 檢查公司是否啟用定位服務
            if user.company.location_service_enabled:
                self.pending_actions[user_id] = message_text
                self.line_service.request_location(event.reply_token)
            else:
                # 如果沒有啟用定位服務，直接打卡
                if message_text == "上班打卡":
                    response = self.attendance_service.record_clock_in(
                        user_id, 
                        user.display_name,
                        ip_address=request.headers.get('X-Forwarded-For', request.remote_addr)
                    )
                else:
                    response = self.attendance_service.record_clock_out(
                        user_id, 
                        user.display_name,
                        ip_address=request.headers.get('X-Forwarded-For', request.remote_addr)
                    )
                self.line_service.send_text_message(event.reply_token, response)
        elif message_text == "查詢打卡":
            response = self.attendance_service.get_attendance_record(user_id)
            self.line_service.send_text_message(event.reply_token, response)
        else:
            self.line_service.send_text_message(
                event.reply_token,
                "請輸入：上班打卡、下班打卡 或 查詢打卡"
            )

# 創建全局實例
message_handler = MessageHandler()

def handle_message(event):
    return message_handler.handle_message(event)