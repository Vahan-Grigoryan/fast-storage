from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Boolean,
    Column,
)


engine = create_engine("sqlite:///db\db.sqlite")

Base = declarative_base()
Base.metadata.reflect(engine)


class TMPData(Base):
    """Model for storing plain text in data column"""

    __tablename__ = "tmpdata"
    __table_args__ = {
        "extend_existing":True
    }

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(String, nullable=False)
    important = Column(Boolean, default=False, nullable=False)
    urgently = Column(Boolean, default=False, nullable=False)


Base.metadata.create_all(engine)

