from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

#Define credentials

username = 'fake_user'

password = 'fake'

host = '127.0.0.1'

port = int(5432)

database = 'fake_db'

DATABASE_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URI, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()