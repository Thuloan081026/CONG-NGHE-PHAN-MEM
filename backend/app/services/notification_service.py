from workers.notification_task import send_notification_task

class NotificationService:

    @staticmethod
    def notify_followers(syllabus_id: int, message: str):
        send_notification_task.delay(syllabus_id, message)

    @staticmethod
    def notify_lecturer(lecturer_id: int, message: str):
        send_notification_task.delay(lecturer_id, message)
