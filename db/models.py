from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(20000), index=True, nullable=True)
    call_id = Column(String, nullable=True)
    generated = Column(Boolean, default=False)
    uuid = Column(String, nullable=True)