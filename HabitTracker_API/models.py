import uuid
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, Boolean, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    profile_image_key = Column(String, nullable=True)

    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")

class Habit(Base):
    __tablename__ = "habits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, index=True, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="habits")
