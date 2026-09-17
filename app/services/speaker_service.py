from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.speaker import Speaker
from app.repositories.speaker_repository import SpeakerRepository
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate


class SpeakerService:

    @staticmethod
    def create_speaker(
        db: Session,
        data: SpeakerCreate
    ):

        existing = SpeakerRepository.get_by_email(
            db,
            data.email
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Speaker with this email already exists"
            )

        speaker = Speaker(
            name=data.name,
            email=data.email,
            phone=data.phone,
            bio=data.bio,
            expertise=data.expertise,
            company=data.company,
            experience=data.experience,
            is_active=True
        )

        return SpeakerRepository.create(db, speaker)

    @staticmethod
    def get_speakers(db: Session):
        return SpeakerRepository.get_all(db)

    @staticmethod
    def get_speaker(
        db: Session,
        speaker_id: int
    ):

        speaker = SpeakerRepository.get_by_id(
            db,
            speaker_id
        )

        if not speaker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Speaker not found"
            )

        return speaker

    @staticmethod
    def update_speaker(
        db: Session,
        speaker_id: int,
        data: SpeakerUpdate
    ):

        speaker = SpeakerService.get_speaker(
            db,
            speaker_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:

            existing = SpeakerRepository.get_by_email(
                db,
                update_data["email"]
            )

            if existing and existing.id != speaker_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another speaker already uses this email"
                )

        return SpeakerRepository.update(
            db,
            speaker,
            update_data
        )

    @staticmethod
    def delete_speaker(
        db: Session,
        speaker_id: int
    ):

        speaker = SpeakerService.get_speaker(
            db,
            speaker_id
        )

        SpeakerRepository.delete(
            db,
            speaker
        )

    @staticmethod
    def activate_speaker(
        db: Session,
        speaker_id: int
    ):

        speaker = SpeakerService.get_speaker(
            db,
            speaker_id
        )

        return SpeakerRepository.set_active(
            db,
            speaker,
            True
        )

    @staticmethod
    def deactivate_speaker(
        db: Session,
        speaker_id: int
    ):

        speaker = SpeakerService.get_speaker(
            db,
            speaker_id
        )

        return SpeakerRepository.set_active(
            db,
            speaker,
            False
        )