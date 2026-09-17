from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.services.notification_service import (
    NotificationService,
)

from app.utils.enums import NotificationType


notification_service = NotificationService()


def send_background_notification(
    background_tasks: BackgroundTasks,
    db: Session,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    message: str,
):

    notification = notification_service.create_notification(
        db=db,
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
    )

    background_tasks.add_task(
        notification_service.send_notification,
        db,
        notification.id,
    )

    return notification