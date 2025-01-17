from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, LocationMessage
import os
from app.handlers.message_handler import handle_message
from app.models.user import User
from app.models.company import Company
from app.models.attendance import Attendance
from app.utils.database import db
from app.services.line_service import LineService

# 初始化服務
line_service = LineService(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化數據庫
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return 'Line Attendance Bot is running!'
    
    @app.route("/callback", methods=['POST'])
    def callback():
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        
        try:
            handler.handle(body, signature)
        except Exception as e:
            print(f"Error handling webhook: {str(e)}")
            abort(400)
            
        return 'OK'

    # 註冊 LINE Bot 的訊息處理器
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        handle_message(event)

    @handler.add(MessageEvent, message=LocationMessage)
    def handle_location_message(event):
        handle_message(event)
    
    return app
