from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

# 創建全局 SQLAlchemy 實例
db = SQLAlchemy()

class Database:
    def __init__(self):
        # 使用環境變數中的配置構建數據庫 URL
        host = os.getenv('POSTGRES_HOST')
        db_name = os.getenv('POSTGRES_DB')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        
        database_url = f"postgresql://{user}:{password}@{host}/{db_name}"
        
        try:
            self.engine = create_engine(database_url)
        except Exception as e:
            print(f"數據庫連接錯誤: {str(e)}")
            raise
