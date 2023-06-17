from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base


class User(Base):
    __tablename__ = "" # あとでかく

    point_type = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

    class Config:
        orm_mode = True