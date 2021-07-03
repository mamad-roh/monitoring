from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base


class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=True, unique=True)
    phone = Column(String(14), nullable=True, unique=True)
    email = Column(String(50), nullable=True, unique=True)
    telegram_id = Column(String(20), nullable=True, unique=True)
    is_active = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)

    # items = relationship("ContactModel", back_populates="owner")

    child_contact = relationship(
        'ManageServer',
        back_populates='parant_contact',
        cascade="all, delete"
    )
