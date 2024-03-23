from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Column,
)


Base = declarative_base()

class TMPData(Base):
    """Model for storing plain text in data column"""

    __tablename__ = "tmpdata"

    id = Column(Integer, primary_key=True)
    data = Column(String, nullable=False)
    important = Column(Boolean, default=False, nullable=False)
    urgently = Column(Boolean, default=False, nullable=False)


