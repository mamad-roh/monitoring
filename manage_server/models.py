# from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base


class ManageServer(Base):
    __tablename__ = 'ManageServer'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    # owner = relationship("UserModel", back_populates="items")
