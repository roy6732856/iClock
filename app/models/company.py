from app.utils.database import db

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)  # 用於匹配的公司代碼
    latitude = db.Column(db.Float, nullable=True)  # 緯度
    longitude = db.Column(db.Float, nullable=True)  # 經度
    address = db.Column(db.String(200), nullable=True)  # 地址
    clock_in_radius = db.Column(db.Float, default=0.1)  # 打卡範圍（公里）
    location_service_enabled = db.Column(db.Boolean, default=False)  # 新增欄位：是否啟用定位服務
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    users = db.relationship('User', backref='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.name}>' 