from sqlalchemy import Column, Integer, String
from db.database import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(20000), index=True)
