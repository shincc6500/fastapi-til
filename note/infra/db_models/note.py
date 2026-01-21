from database.database import Base
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

note_tag_associaton = Table(
    "Note_Tag",
    Base.metadata, 
    Column("note_id", String(36),ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)

class Note(Base):
    __tablename__ = "Note"
    # TODO : user 쪽 테이블과 같은 mapped 양식으로 리펙토링 예정. 리펙토링만으로는 마이그래이션 다시 할 필요 없음. 

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at= Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    tags = relationship(
        "Tag",
        secondary=note_tag_associaton, 
        back_populates="notes",
        lazy = "joined",
    )

class Tag(Base):
    __tablename__ = "Tag"

    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable = False, unique=True)
    created_at= Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    notes = relationship(
        "Note",
        secondary=note_tag_associaton, 
        back_populates="tags",
        lazy = "joined",
    )