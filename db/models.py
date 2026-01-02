from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db.database import Base



class DbPost(Base):
    __tablename__: str = "post"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique identifier for the post (Auto-incrementing PK).",
    )
    text: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        comment="The post's text.",
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=False,
        index=True,
        comment="Unique identifier for the post owner.",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of when the post was created.",
    )
