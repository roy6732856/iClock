from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
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
from app.routes.auth import auth_bp

# 初始化服務
line_service = LineService(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 啟用 CORS
    CORS(app, 
        resources={
            r"/api/*": {
                "origins": ["http://localhost:8080", "http://127.0.0.1:8080", 
                           "http://localhost:5173", "http://127.0.0.1:5173",
                           "http://localhost:8000", "http://127.0.0.1:8000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Authorization"],
                "max_age": 600
            }
        },
        supports_credentials=True
    )

    # 添加 CORS headers 到所有回應
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')  # 添加更多允許的 headers
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        # 明確設置 Content-Type
        if request.method == 'OPTIONS':
            response.headers['Content-Type'] = 'application/json'
        return response
    
    # 初始化數據庫
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 註冊 auth blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    with app.app_context():
        db.create_all()
        line_service.create_rich_menu()  # 創建 Rich Menu
    
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
