from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        # 從環境變數獲取資料庫配置
        host = os.getenv('POSTGRES_HOST')
        db = os.getenv('POSTGRES_DB')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')

        # 組合 PostgreSQL 連線字串
        database_url = f"postgresql://{user}:{password}@{host}/{db}"

        if not all([host, db, user, password]):
            raise ValueError("Missing database configuration in environment variables")

        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            # 如果需要 SSL 連線（AWS RDS 通常需要）
            connect_args={
                "sslmode": "require"
            }
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self._initialized = True

    def get_session(self):
        return self.SessionLocal()

    def init_database(self):
        """初始化資料庫連接"""
        try:
            # 不再自動刪除和創建表
            # 改用 alembic 管理資料庫結構
            print("資料庫連接已初始化")
        except Exception as e:
            print(f"初始化資料庫時發生錯誤: {str(e)}")
            raise
