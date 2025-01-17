from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_rich_menu_image():
    # 創建一個新的圖片，使用淺灰色背景
    img = Image.new('RGB', (2500, 843), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加背景設計元素
    # 左側L形裝飾
    draw.rectangle([(50, 50), (200, 200)], fill='#FFD700')  # 黃金色
    draw.rectangle([(50, 50), (100, 300)], fill='#FFD700')
    
    # 右上角X形裝飾
    draw.line([(2300, 50), (2450, 200)], fill='#FFD700', width=15)
    draw.line([(2450, 50), (2300, 200)], fill='#FFD700', width=15)
    
    # 右下角圓形裝飾
    draw.ellipse([(2300, 643), (2450, 793)], fill='#FFD700')
    
    # 左上角圓點和線條
    draw.ellipse([(50, 50), (100, 100)], fill='#FFD700')
    for i in range(7):
        draw.line([(120 + i*20, 75), (220 + i*20, 75)], fill='#FFD700', width=3)
    
    # 畫三個區域的分隔線
    draw.line([(833, 0), (833, 843)], fill='#E0E0E0', width=2)
    draw.line([(1666, 0), (1666, 843)], fill='#E0E0E0', width=2)
    
    # 嘗試載入中文字體
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "C:/Windows/Fonts/msjh.ttc",  # Windows 微軟正黑體
        "C:/Windows/Fonts/mingliu.ttc",  # Windows 細明體
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 60)
            break
        except:
            continue
    
    if font is None:
        print("警告：找不到合適的中文字體，將使用默認字體")
        font = ImageFont.load_default()
    
    # 為每個按鈕區域添加圓角矩形背景
    def draw_rounded_rectangle(x, y, width, height, radius, color):
        draw.rectangle([(x+radius, y), (x+width-radius, y+height)], fill=color)
        draw.rectangle([(x, y+radius), (x+width, y+height-radius)], fill=color)
        draw.ellipse([(x, y), (x+2*radius, y+2*radius)], fill=color)
        draw.ellipse([(x+width-2*radius, y), (x+width, y+2*radius)], fill=color)
        draw.ellipse([(x, y+height-2*radius), (x+2*radius, y+height)], fill=color)
        draw.ellipse([(x+width-2*radius, y+height-2*radius), (x+width, y+height)], fill=color)
    
    # 添加按鈕背景和文字
    button_areas = [
        (266, 371, 300, 100, "上班打卡"),
        (1099, 371, 300, 100, "下班打卡"),
        (1933, 371, 300, 100, "查詢打卡")
    ]
    
    for x, y, width, height, text in button_areas:
        draw_rounded_rectangle(x, y, width, height, 20, '#FFD700')
        draw.text((x + width//2, y + height//2), text, 
                 fill='black', font=font, anchor="mm")
    
    # 確保目錄存在
    base_dir = Path(__file__).parent.parent
    image_dir = os.path.join(base_dir, 'static', 'images')
    os.makedirs(image_dir, exist_ok=True)
    
    # 保存圖片
    image_path = os.path.join(image_dir, 'rich_menu.png')
    img.save(image_path)
    print(f"Rich Menu 圖片已創建: {image_path}")

if __name__ == "__main__":
    create_rich_menu_image()
