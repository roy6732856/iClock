from app.utils.database import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    display_name = db.Column(db.String(100))
    clock_in_time = db.Column(db.DateTime, nullable=True)
    clock_out_time = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.Date, default=db.func.current_timestamp())
    
    # 新增欄位
    clock_in_ip = db.Column(db.String(50), nullable=True)
    clock_out_ip = db.Column(db.String(50), nullable=True)
    clock_in_location = db.Column(db.String(200), nullable=True)
    clock_out_location = db.Column(db.String(200), nullable=True)

    user = db.relationship('User', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.user_id} - {self.date}>'