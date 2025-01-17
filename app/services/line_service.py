from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction

class LineService:
    def __init__(self, channel_access_token):
        self.line_bot_api = LineBotApi(channel_access_token)

    def send_text_message(self, reply_token, text):
        """發送文字消息"""
        self.line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=text)
        )

    def request_location(self, reply_token):
        """請求位置信息"""
        location_request = TemplateSendMessage(
            alt_text='請分享位置',
            template=ButtonsTemplate(
                title='打卡需要位置信息',
                text='請分享您的位置',
                actions=[
                    URIAction(
                        label='分享位置',
                        uri='line://nv/location'
                    )
                ]
            )
        )
        self.line_bot_api.reply_message(reply_token, location_request)

    def get_profile(self, user_id):
        """獲取用戶資料"""
        return self.line_bot_api.get_profile(user_id)