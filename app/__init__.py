from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import os
from app.handlers.message_handler import handle_message
from app.models.attendance import Base

# 初始化 SQLAlchemy 和 LINE handler
db = SQLAlchemy()
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        from app.utils.database import Database
        engine = Database().engine
        Base.metadata.create_all(engine)
    
    @app.route('/')
    def home():
        return 'Line Attendance Bot is running!'
    
    @app.route("/callback", methods=['POST'])
    def callback():
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
            
        return 'OK'

    # 註冊 LINE Bot 的訊息處理器
    @handler.add(MessageEvent, message=TextMessage)
    def message_text(event):
        handle_message(event)
    
    return app
