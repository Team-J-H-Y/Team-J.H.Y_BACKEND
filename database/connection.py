import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker


# 프로젝트 최상위 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 프로젝트 최상위의 .env 파일 읽기
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


# SQLAlchemy Engine 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# DB Session 생성기
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


# 연결 테스트용 함수
def test_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("MySQL 연결 성공")


if __name__ == "__main__":
    test_connection()