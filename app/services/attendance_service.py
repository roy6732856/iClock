from datetime import datetime, date
from contextlib import contextmanager
from app.utils.database import Database
from app.models.attendance import Attendance

class AttendanceService:
    def __init__(self):
        self.db = Database()

    @contextmanager
    def get_session(self):
        session = self.db.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def record_clock_in(self, user_id, user_name):
        try:
            with self.get_session() as session:
                today = date.today()
                existing_record = session.query(Attendance).filter(
                    Attendance.user_id == user_id,
                    Attendance.date == today
                ).first()

                if existing_record and existing_record.clock_in:
                    return "您今天已經上班打卡了！"

                if existing_record:
                    existing_record.clock_in = datetime.now()
                else:
                    new_record = Attendance(
                        user_id=user_id,
                        user_name=user_name,
                        date=today,
                        clock_in=datetime.now()
                    )
                    session.add(new_record)

                return f"上班打卡成功！時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        except Exception as e:
            print(f"打卡錯誤: {str(e)}")
            return "打卡失敗，請稍後再試"

    def record_clock_out(self, user_id, user_name):
        try:
            with self.get_session() as session:
                today = date.today()
                record = session.query(Attendance).filter(
                    Attendance.user_id == user_id,
                    Attendance.date == today
                ).first()

                if not record:
                    return "您今天還沒有上班打卡！"

                if record.clock_out:
                    return "您今天已經下班打卡了！"

                record.clock_out = datetime.now()
                record.user_name = user_name
                return f"下班打卡成功！時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        except Exception as e:
            print(f"打卡錯誤: {str(e)}")
            return "打卡失敗，請稍後再試"

    def get_attendance_record(self, user_id):
        try:
            with self.get_session() as session:
                today = date.today()
                record = session.query(Attendance).filter(
                    Attendance.user_id == user_id,
                    Attendance.date == today
                ).first()

                if not record:
                    return "今天還沒有打卡記錄"

                result = f"今日打卡記錄：\n"
                result += f"姓名：{record.user_name}同學\n"
                if record.clock_in:
                    result += f"上班時間：{record.clock_in.strftime('%H:%M:%S')}\n"
                if record.clock_out:
                    result += f"下班時間：{record.clock_out.strftime('%H:%M:%S')}"

                return result

        except Exception as e:
            print(f"查詢錯誤: {str(e)}")
            return "查詢失敗，請稍後再試"
