import threading
import time
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import requests


# engine = create_engine("sqlite:///:memory:", echo=False)
engine = create_engine("mysql+pymysql://new_user:1@127.0.0.1:3306/new_db", echo=False)

Base = declarative_base()


class DownloaderTb(Base):
    __tablename__ = 'downloaderTB'
    id = Column(Integer, primary_key=True)
    url = Column(String(250))
    createdAT = Column(DateTime(timezone=True), server_default=func.now())
    path = Column(String(250))
    status = Column(Integer)


Base.metadata.create_all(engine)

DBsession = sessionmaker(bind=engine)
session = DBsession()


# ina baraye sakht (insert)
# u1 = DownloaderTb(
#     url="https://www.google.com/",
#     path='/home/mobina/happy',
#     status=1
# )
# #
# session.add(u1)
# session.commit()

# result = session.query(DownloaderTb)
# for data in result:
# print(data.url, data.createdAT)
# print(result.__dict__)

class Getinput():
    url_input = input("enter the url: ")
    path_input = input("enter the path: ")
    status_input = int(input("enter the status: "))

    if path_input == '':
        new_d = DownloaderTb(url=url_input,
                             path="/home/mobina/happy",
                             status=status_input,)
        session.add(new_d)
        session.commit()

    elif status_input == 0:
        new_k = DownloaderTb(url=url_input,
                             path=path_input,
                             status=1, )
        session.add(new_k)
        session.commit()

    else:
        new_m = DownloaderTb(url=url_input,
                             path=path_input,
                             status=status_input,)
        session.add(new_m)
        session.commit()


def download_url(data):
    if data.status_input == 1:
        session.query(DownloaderTb).update({DownloaderTb.status: 2})
        session.commit()
        try:
            basename = os.path.basename(data.url_input)
            response = requests.get(data.url_input)
            open(basename, "wb").write(response.content)
        except OSError:
            session.query(DownloaderTb).update({DownloaderTb.status: 3})
            session.commit()

        else:
            session.query(DownloaderTb).update({DownloaderTb.status: 4})
            session.commit()


def run():
    while True:
        time.sleep(0.1)
        threads = []
        result = session.query(Getinput)
        for data in result:
            thread = threading.Thread(target=download_url(data))
            thread.start()
            threads.append(thread)
            for thread in threads:
                thread.join()

download_url(data=)