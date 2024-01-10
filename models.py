from sqlalchemy import String, Integer, Column, Boolean

from database import Base, engine

def create_tables():
    Base.metadata.create_all(engine)


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    age = Column(Integer)
    is_male = Column(Boolean)
