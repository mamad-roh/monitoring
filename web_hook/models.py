from sqlalchemy import Boolean, Column, Integer, String
from database.database import Base


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    host_ip = Column(String(50), nullable=False, unique=True)
    token = Column(String, nullable=False)
