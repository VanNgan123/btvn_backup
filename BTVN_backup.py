import os
import shutil
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from sendemail import send_email # Import module send_mail

load_dotenv()
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
BACKUP_DIR = "backup"

def backup_database():
    now = datetime.now()
    timestamp = now.strftime("_%H_%M___%d_%m_%Y")
    backup_successful = True
    error_message = ""

    for file in [f for f in os.listdir('.') if f.endswith(".sql")]:
        backup_filepath = os.path.join(BACKUP_DIR, f"{file}_{timestamp}")
        try:
            shutil.copy2(file, backup_filepath)
            print(f"Đã backup thành công: {file} -> {backup_filepath}")
        except Exception as e:
            print(f"Backup {file} thất bại: {e}")
            backup_successful = False
            error_message += f"Lỗi backup file {file}: {e}\n"

    for file in [f for f in os.listdir('.') if f.endswith(".sqlite3")]:
        backup_filepath = os.path.join(BACKUP_DIR, f"{file}_{timestamp}")
        try:
            shutil.copy2(file, backup_filepath)
            print(f"Đã backup thành công: {file} -> {backup_filepath}")
        except Exception as e:
            print(f"Backup {file} thất bại: {e}")
            backup_successful = False
            error_message += f"Lỗi backup file {file}: {e}\n"

    if backup_successful:
        return True, "Backup thành công"
    else:
        return False, f"Backup thất bại:\n{error_message}"

def job():
    print("Bắt đầu công việc backup...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    success, message = backup_database()
    subject = "Thông báo Backup Database"
    body = message
    send_email(RECEIVER_EMAIL, subject, body)
    print("Hoàn thành công việc backup.")

if __name__ == "__main__":
    schedule.every().day.at("00:00").do(job)
    print("Lịch backup đã được thiết lập để chạy vào 00:00 hàng ngày.")
    while True:
        schedule.run_pending()
        time.sleep(1)