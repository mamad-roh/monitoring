from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base


class ManageServer(Base):
    __tablename__ = 'manage_server'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey(
        'servers.id', ondelete='CASCADE'
        ), nullable=False)

    contact_id = Column(Integer, ForeignKey(
        'contacts.id', ondelete='CASCADE'
        ), nullable=False)

    parant_server = relationship(
        'ServerModel',
        back_populates='child_server'
    )
    parant_contact = relationship(
        'ContactModel',
        back_populates='child_contact'
    )

    child_manage_server = relationship(
        'MediaManageModel',
        back_populates='parant_manage_server',
        cascade="all, delete"
    )
