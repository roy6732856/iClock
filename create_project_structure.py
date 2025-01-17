# create_project_structure.py
import os

def create_directory_structure():
    # 定義要創建的目錄
    directories = [
        'app',
        'app\\models',
        'app\\services',
        'app\\utils',
        'app\\handlers',
        'tests',
        'migrations'
    ]
    
    # 創建目錄
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f'Created directory: {directory}')

# 檔案結構定義
structure = {
    '.env': '''
POSTGRES_HOST=your-rds-endpoint
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
LINE_CHANNEL_ACCESS_TOKEN=your-token
LINE_CHANNEL_SECRET=your-secret
DEBUG=True
''',
    
    'requirements.txt': '''
flask==2.0.1
python-dotenv==0.19.0
psycopg2-binary==2.9.1
line-bot-sdk==2.0.1
SQLAlchemy==1.4.23
Flask-SQLAlchemy==2.5.1
alembic==1.7.1
''',
    
    'run.py': '''
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',
    
    '.gitignore': '''
# Virtual Environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class

# Environment variables
.env

# IDE
.vscode/
.idea/

# Database
*.db
*.sqlite3

# Logs
*.log
''',
    
    'app\\__init__.py': '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from app.handlers import register_handlers
    register_handlers(app)
    
    return app
''',
    
    'app\\config.py': '''
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
''',
    
    'app\\models\\__init__.py': '',
    'app\\models\\employee.py': '''
from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
''',
    
    'app\\models\\attendance.py': '''
from app import db
from datetime import datetime

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    punch_time = db.Column(db.DateTime, default=datetime.utcnow)
    punch_type = db.Column(db.String(10))
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    ip_address = db.Column(db.String(45))
''',
    
    'app\\services\\__init__.py': '',
    'app\\services\\line_service.py': '''
from linebot import LineBotApi, WebhookHandler
from app.config import Config

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
''',
    
    'app\\handlers\\__init__.py': '''
from flask import request, abort
from app.services.line_service import handler
from linebot.exceptions import InvalidSignatureError

def register_handlers(app):
    @app.route("/callback", methods=['POST'])
    def callback():
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
            
        return 'OK'
        
    from . import message_handler  # 註冊訊息處理器
''',
    
    'app\\handlers\\message_handler.py': '''
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.services.line_service import line_bot_api, handler

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    
    if text == "打卡":
        reply_text = "打卡功能開發中..."
    else:
        reply_text = "請使用正確的指令"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
''',

    'app\\utils\\__init__.py': '',
    'tests\\__init__.py': '',
}

def create_files():
    # 首先創建目錄結構
    create_directory_structure()
    
    # 然後創建檔案
    for file_path, content in structure.items():
        # 如果檔案路徑是空的，跳過
        if not file_path:
            continue
            
        # 確保目錄存在
        dir_name = os.path.dirname(file_path)
        if dir_name:  # 只在有目錄路徑時創建
            os.makedirs(dir_name, exist_ok=True)
        
        # 寫入檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
            print(f'Created file: {file_path}')

if __name__ == '__main__':
    create_files()
