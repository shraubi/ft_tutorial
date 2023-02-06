from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class samples(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    prompt = Column(String)
    answers = Column(String)


def get_engine():
    return create_engine(
        "sqlite:///samples.db", connect_args={"check_same_thread": False}
    )


def get_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def create_table(engine):
    Base.metadata.create_all(engine, checkfirst=True)
