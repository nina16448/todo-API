# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用 SQLite 本地資料庫（部署再改 PostgreSQL）
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:knZRvTUjbxsJiVfutoFxUxiFGjcppMtQ@caboose.proxy.rlwy.net:18254/railway"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
