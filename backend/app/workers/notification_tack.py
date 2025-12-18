from celery import Celery
import smtplib

app = Celery("notification", broker="redis://localhost:6379/0")

@app.task(name="notification.send")
def send_notification_task(target_id: int, message: str):
    # TODO: Query DB -> lấy email người theo dõi syllabus hoặc lecturer
    
    print(f"[NOTIFICATION] Send to {target_id}: {message}")

    # Ví dụ gửi email thật:
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login("your-email", "app-password")
    # server.sendmail("your-email", receiver_email, message)

    return True
