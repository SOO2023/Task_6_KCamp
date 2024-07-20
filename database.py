from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL = "sqlite:///.database.db"
engine = create_engine(url=URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def db_session():
    try:
        session = sessionLocal()
        yield session
    finally:
        session.close()
