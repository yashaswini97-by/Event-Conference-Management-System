from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.utils.enums import NotificationStatus


class NotificationRepository:

    def create(
        self,
        db: Session,
        notification: Notification,
    ):
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    def get_by_id(
        self,
        db: Session,
        notification_id: int,
    ):
        return db.query(Notification).filter(
            Notification.id == notification_id
        ).first()

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
    ):
        return db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def get_unread_notifications(
        self,
        db: Session,
        user_id: int,
    ):
        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def mark_as_read(
        self,
        db: Session,
        notification: Notification,
    ):
        notification.is_read = True
        notification.read_at = datetime.utcnow()

        db.commit()
        db.refresh(notification)

        return notification

    def mark_all_as_read(
        self,
        db: Session,
        user_id: int,
    ):
        notifications = db.query(
            Notification
        ).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
        ).all()

        now = datetime.utcnow()

        for notification in notifications:
            notification.is_read = True
            notification.read_at = now

        db.commit()

        return len(notifications)

    def update_status(
        self,
        db: Session,
        notification: Notification,
        status: NotificationStatus,
    ):
        notification.status = status

        if status == NotificationStatus.SENT:
            notification.sent_at = datetime.utcnow()

        db.commit()
        db.refresh(notification)

        return notification