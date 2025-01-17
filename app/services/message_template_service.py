class MessageTemplateService:
    @staticmethod
    def create_main_menu():
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "打卡系統",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "action": {
                                    "type": "message",
                                    "label": "上班打卡",
                                    "text": "上班打卡"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "message",
                                    "label": "下班打卡",
                                    "text": "下班打卡"
                                }
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "margin": "md",
                        "action": {
                            "type": "message",
                            "label": "查詢記錄",
                            "text": "查詢打卡"
                        }
                    }
                ]
            }
        }

    @staticmethod
    def create_quick_reply():
        return {
            "items": [
                {
                    "type": "action",
                    "action": {
                        "type": "message",
                        "label": "上班打卡",
                        "text": "上班打卡"
                    }
                },
                {
                    "type": "action",
                    "action": {
                        "type": "message",
                        "label": "下班打卡",
                        "text": "下班打卡"
                    }
                },
                {
                    "type": "action",
                    "action": {
                        "type": "message",
                        "label": "查詢記錄",
                        "text": "查詢打卡"
                    }
                }
            ]
        }

    @staticmethod
    def create_attendance_record(records):
        contents = []
        for record in records:
            record_box = {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"日期：{record.date}",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"上班時間：{record.clock_in_time.strftime('%H:%M:%S')}",
                        "size": "sm"
                    }
                ]
            }
            
            if record.clock_out_time:
                record_box["contents"].append({
                    "type": "text",
                    "text": f"下班時間：{record.clock_out_time.strftime('%H:%M:%S')}",
                    "size": "sm"
                })
            
            contents.append(record_box)

        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "打卡記錄",
                        "weight": "bold",
                        "size": "lg"
                    },
                    *contents
                ]
            }
        } 