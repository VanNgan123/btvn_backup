import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


print(f"Giá trị SENDER_EMAIL: {SENDER_EMAIL}")
print(f"Giá trị SENDER_PASSWORD: {SENDER_PASSWORD}")
def send_email(receiver, subject, body):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, receiver, text)
        print(f"Email đã được gửi đến {receiver}")
    except Exception as e:
        print(f"Gửi email thất bại: {e}")

