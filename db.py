from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://new_user:1@127.0.0.1:3306/new_db", echo=False)
Base = declarative_base()

STATUS_NEW = 1
STATUS_DOWNLOADING = 2
STATUS_FAIL = 3
STATUS_COMPLETE = 4


class DownloaderTb(Base):
    __tablename__ = 'downloaderTB'
    id = Column(Integer, primary_key=True)
    url = Column(String(250))
    createdAT = Column(DateTime(timezone=True), server_default=func.now())
    path = Column(String(250))
    status = Column(Integer)
    error = Column(String(1000))


DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
