from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.connections.database import Base
from app.constants import TableName


ioc_tag = Table(
    TableName.IOC_TAG.value,
    Base.metadata,
    Column("ioc_id", Integer, ForeignKey(f"{TableName.IOC.value}.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey(f"{TableName.TAG.value}.id", ondelete="CASCADE"), primary_key=True),
)


class IOC(Base):
    __tablename__ = TableName.IOC.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    ioc_type = Column(String(20), nullable=False)
    ioc_raw = Column(Text, nullable=False)
    ioc_canonical = Column(Text, nullable=False, unique=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tags = relationship(
        "Tag",
        secondary=ioc_tag,
        back_populates="iocs",
        lazy="selectin",
    )
