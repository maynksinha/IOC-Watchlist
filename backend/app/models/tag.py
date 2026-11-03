from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.connections.database import Base
from app.constants import TableName
from .ioc import ioc_tag


class Tag(Base):
    __tablename__ = TableName.TAG.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    iocs = relationship(
        "IOC",
        secondary=ioc_tag,
        back_populates="tags",
        lazy="selectin",
    )
