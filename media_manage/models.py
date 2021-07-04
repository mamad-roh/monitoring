from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import String
from database.database import Base


class MediaManageModel(Base):
    __tablename__ = 'media_manage'

    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey(
        'media.id', ondelete='CASCADE'
        ), nullable=False)
    detail = Column(String, nullable=True)

    manage_server_id = Column(Integer, ForeignKey(
        'manage_server.id', ondelete='CASCADE'
        ), nullable=False)

    parant_media = relationship(
        'MediaModel',
        back_populates='child_media_manage'
    )
    parant_manage_server = relationship(
        'ManageServer',
        back_populates='child_manage_server'
    )
