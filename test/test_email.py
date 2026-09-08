import os
import ssl
import smtplib
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 최상위 폴더 경로
BASE_DIR = Path(__file__).resolve().parent.parent

#.env 파일 읽기
load_dotenv(BASE_DIR / ".env")

# .env에서 발송 메일 정보 가져오기
sender_email = os.getenv("GMAIL_ADDRESS")
password = os.getenv("GMAIL_APP_PASSWORD")


context = ssl.create_default_context()

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465,
    context=context,
    timeout=10,
) as smtp:
    smtp.login(sender_email, password)

print("SMTP 인증 성공")