from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# this is the Alembic Config object
config = context.config

# 設置資料庫 URL
config.set_main_option('sqlalchemy.url', 
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}")

# 添加模型的 metadata
from app.utils.database import db
target_metadata = db.metadata