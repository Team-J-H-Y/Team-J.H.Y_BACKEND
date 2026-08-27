import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

# 프로젝트 최상위 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

#.env 파일 읽기
load_dotenv(BASE_DIR / ".env")

# .env에서 MySQL 접속 정보 가져오기
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# SQLAlchemy가 사용할 MySQL 접속 주소 생성
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# DB 연결 관리자 생성
engine = create_engine(DATABASE_URL)

#서버 연결 테스트
"""
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())
"""

# DB Session(작업 관리자) 생성기
SessionLocal = sessionmaker(bind=engine)

# DB Session을 생성하고 반환하는 함수
def Create_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

