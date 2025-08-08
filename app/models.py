from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Boolean, String, ForeignKey, Integer, text

from .database import Base  # 从 database.py 导入你的 Declarative Base


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    published = mapped_column(Boolean, server_default='True', nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")  # related to User model

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    phone_number = mapped_column(String)
    # posts: Mapped[list[Post]] = relationship("Post", back_populates="owner")  # related to Post model

class Vote(Base):
    __tablename__ = 'votes'
    user_id = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True, nullable=False)
    post_id = mapped_column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True, nullable=False)