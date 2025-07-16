import uuid

from sqlalchemy import (
    Column,
    DateTime,
    func,
    UUID,
    TEXT,
    ForeignKey,
    Integer,
    CHAR,
)
from sqlalchemy.dialects.postgresql import JSONB

from models.base import Base


class ChatSession(Base):
    __tablename__ = 'chat_session'
    __table_args__ = {'schema': 'testing'}

    chat_session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('testing.user.id'), nullable=False)
    name = Column(TEXT, nullable=False, server_default='Chat Session')
    metadata_ = Column(JSONB, name='metadata', default=lambda : {})
    created_at = Column(DateTime(timezone=False), server_default=func.timezone('UTC', func.now()))
    last_modified_ts = Column(DateTime(timezone=False), server_default=func.timezone('UTC', func.now()),
                              onupdate = func.timezone('UTC', func.now()))
