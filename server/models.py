from sqlalchemy import Integer, Column, Boolean
from sqlalchemy.sql.sqltypes import String
from database.database import Base
from sqlalchemy.orm import relationship


class ServerModel(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    ip = Column(String, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)

    child_server = relationship(
        'ManageServer',
        back_populates='parant_server',
        cascade="all, delete"
    )
