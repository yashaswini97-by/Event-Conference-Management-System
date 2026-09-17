from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.speaker import Speaker


class SpeakerRepository:

    @staticmethod
    def create(db: Session, speaker: Speaker) -> Speaker:
        db.add(speaker)
        db.commit()
        db.refresh(speaker)
        return speaker

    @staticmethod
    def get_by_id(db: Session, speaker_id: int):
        return db.scalar(
            select(Speaker).where(
                Speaker.id == speaker_id,
                Speaker.is_deleted == False
            )
        )

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.scalar(
            select(Speaker).where(
                Speaker.email == email,
                Speaker.is_deleted == False
            )
        )

    @staticmethod
    def get_all(db: Session):
        return db.scalars(
            select(Speaker)
            .where(Speaker.is_deleted == False)
            .order_by(Speaker.id.desc())
        ).all()

    @staticmethod
    def update(db: Session, speaker: Speaker, data: dict):
        for key, value in data.items():
            setattr(speaker, key, value)

        db.commit()
        db.refresh(speaker)

        return speaker

    @staticmethod
    def delete(db: Session, speaker: Speaker):
        speaker.is_deleted = True
        db.commit()

    @staticmethod
    def set_active(
        db: Session,
        speaker: Speaker,
        active: bool
    ):
        speaker.is_active = active

        db.commit()
        db.refresh(speaker)

        return speaker