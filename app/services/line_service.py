from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, 
    TemplateSendMessage, 
    ButtonsTemplate, 
    URIAction,
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    RichMenu,
    RichMenuArea,
    RichMenuBounds
)
from app.services.message_template_service import MessageTemplateService
import os
from pathlib import Path

class LineService:
    def __init__(self, channel_access_token):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.template_service = MessageTemplateService()
        # 獲取當前文件所在目錄的根目錄
        self.base_dir = Path(__file__).parent.parent

    def send_text_message(self, reply_token, text):
        """發送文字消息"""
        message = TextSendMessage(
            text=text,
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="上班打卡", text="上班打卡")),
                QuickReplyButton(action=MessageAction(label="下班打卡", text="下班打卡")),
                QuickReplyButton(action=MessageAction(label="查詢記錄", text="查詢打卡"))
            ])
        )
        self.line_bot_api.reply_message(reply_token, message)

    def send_main_menu(self, reply_token):
        """發送主選單"""
        message = FlexSendMessage(
            alt_text="打卡系統選單",
            contents=self.template_service.create_main_menu()
        )
        self.line_bot_api.reply_message(reply_token, message)

    def send_attendance_record(self, reply_token, records):
        """發送打卡記錄"""
        message = FlexSendMessage(
            alt_text="打卡記錄",
            contents=self.template_service.create_attendance_record(records)
        )
        self.line_bot_api.reply_message(reply_token, message)

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

    def create_rich_menu(self):
        try:
            # 刪除現有的 Rich Menu（如果有的話）
            rich_menu_list = self.line_bot_api.get_rich_menu_list()
            for rich_menu in rich_menu_list:
                self.line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

            # 定義 Rich Menu 的區域
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=MessageAction(label="上班打卡", text="上班打卡")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                    action=MessageAction(label="下班打卡", text="下班打卡")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1666, y=0, width=834, height=843),
                    action=MessageAction(label="查詢打卡", text="查詢打卡")
                )
            ]

            # 創建 Rich Menu 對象
            rich_menu_to_create = RichMenu(
                size={"width": 2500, "height": 843},
                selected=True,  # 設置為 True，使其默認顯示
                name="打卡選單",
                chat_bar_text="打卡選單",
                areas=areas
            )

            # 創建 Rich Menu
            rich_menu_id = self.line_bot_api.create_rich_menu(rich_menu_to_create)

            # 上傳圖片
            image_path = os.path.join(self.base_dir, 'static', 'images', 'rich_menu.png')
            if not os.path.exists(image_path):
                print(f"Rich Menu 圖片不存在: {image_path}")
                return
                
            with open(image_path, 'rb') as f:
                self.line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

            # 將 Rich Menu 設為默認
            self.line_bot_api.set_default_rich_menu(rich_menu_id)
            print("Rich Menu 創建成功！")
            
        except Exception as e:
            print(f"創建 Rich Menu 時發生錯誤: {str(e)}")