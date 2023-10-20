import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'), echo=False)
Base = declarative_base()


class Files(Base):
    STATUS_NEW = 1
    STATUS_DOWNLOADING = 2
    STATUS_FAIL = 3
    STATUS_COMPLETE = 4

    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    url = Column(String(250))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    path = Column(String(250), default=os.getenv('DEFAULT_DOWNLOAD_PATH'))
    status = Column(Integer, default=STATUS_NEW)
    error = Column(String(1000), nullable=True)


DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)

