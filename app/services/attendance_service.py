from datetime import datetime
from app.utils.database import db
from app.models.attendance import Attendance
from app.models.user import User
from app.services.location_service import LocationService

class AttendanceService:
    def __init__(self):
        self.location_service = LocationService()

    def record_clock_in(self, line_user_id, display_name, ip_address=None, location=None):
        """記錄上班打卡"""
        user = User.query.filter_by(line_user_id=line_user_id).first()
        if not user:
            return "用戶不存在"

        # 檢查用戶是否已經打卡
        existing_record = Attendance.query.filter_by(
            user_id=user.id,
            date=datetime.now().date(),
            clock_out_time=None
        ).first()
        
        if existing_record:
            return "您已經打過上班卡了！"

        # 檢查公司是否啟用定位服務
        if user.company.location_service_enabled:
            if not location:
                return "請先分享您的位置"
            
            user_location = (location['latitude'], location['longitude'])
            if not self.location_service.is_within_range(user_location, user.company_id):
                return "您不在打卡範圍內！"

        # 創建新的打卡記錄
        new_record = Attendance(
            user_id=user.id,
            display_name=display_name,
            clock_in_time=datetime.now(),
            clock_in_ip=ip_address,
            clock_in_location=str(location) if location else None
        )
        db.session.add(new_record)
        db.session.commit()
        
        return "上班打卡成功！"

    def record_clock_out(self, line_user_id, display_name, ip_address=None, location=None):
        """記錄下班打卡"""
        user = User.query.filter_by(line_user_id=line_user_id).first()
        if not user:
            return "用戶不存在"

        existing_record = Attendance.query.filter_by(
            user_id=user.id,
            date=datetime.now().date(),
            clock_out_time=None
        ).first()
        
        if not existing_record:
            return "您尚未打上班卡！"

        # 檢查公司是否啟用定位服務
        if user.company.location_service_enabled:
            if not location:
                return "請先分享您的位置"
            
            user_location = (location['latitude'], location['longitude'])
            if not self.location_service.is_within_range(user_location, user.company_id):
                return "您不在打卡範圍內！"
            
        existing_record.clock_out_time = datetime.now()
        existing_record.clock_out_ip = ip_address
        existing_record.clock_out_location = str(location) if location else None
        db.session.commit()
        
        return "下班打卡成功！"

    def get_attendance_record(self, line_user_id):
        """獲取打卡記錄"""
        user = User.query.filter_by(line_user_id=line_user_id).first()
        if not user:
            return "用戶不存在"

        records = Attendance.query.filter_by(user_id=user.id).order_by(Attendance.date.desc()).limit(7).all()
        if not records:
            return "沒有打卡記錄。"
        
        response = "您的打卡記錄如下：\n"
        for record in records:
            response += f"- 日期：{record.date}\n"
            response += f"  上班：{record.clock_in_time.strftime('%H:%M:%S')}"
            if record.clock_out_time:
                response += f"\n  下班：{record.clock_out_time.strftime('%H:%M:%S')}"
            response += "\n"
        
        return response
