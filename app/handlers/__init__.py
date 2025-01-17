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