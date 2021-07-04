from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from database.database import Base


class MediaModel(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)

    child_media_manage = relationship(
        'MediaManageModel',
        back_populates='parant_media',
        cascade="all, delete"
    )
