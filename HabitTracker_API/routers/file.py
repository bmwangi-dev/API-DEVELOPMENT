# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

import models
import auth
import storage
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Profile Image"],
)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@router.post("/me/profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file type: {file.content_type}. Allowed: JPEG, PNG, GIF, WebP",
        )

    file_bytes = file.file.read()
    if len(file_bytes) > storage.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"File too large. Maximum size is {storage.MAX_FILE_SIZE // (1024*1024)}MB",
        )

    if current_user.profile_image_key:
        storage.delete_profile_image(current_user.profile_image_key)

    key = storage.upload_profile_image(file_bytes, current_user.id, file.content_type)
    current_user.profile_image_key = key
    db.commit()

    return {
        "profile_image_key": key,
        "profile_image_url": storage.get_profile_image_url(key),
    }


@router.get("/me/profile-image")
def get_profile_image(
    current_user: models.User = Depends(auth.get_current_user),
):
    if not current_user.profile_image_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile image uploaded",
        )

    url = storage.get_profile_image_url(current_user.profile_image_key)
    return {"profile_image_url": url}


@router.delete("/me/profile-image")
def delete_profile_image(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.profile_image_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile image uploaded",
        )

    storage.delete_profile_image(current_user.profile_image_key)
    current_user.profile_image_key = None
    db.commit()

    return {"message": "Profile image deleted successfully."}
