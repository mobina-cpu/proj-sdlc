import os
import threading
import time
from queue import Queue

import requests

from db import Files, session

files_queue = Queue()
checked_id = []

def download_file(file: Files):
    session.query(Files).update({Files.status: Files.STATUS_DOWNLOADING})
    session.commit()

    try:
        basename = os.path.basename(file.url)
        response = requests.get(file.url)
        path = f'{file.path}/{basename}'
        if not os.path.exists(path):
            os.system(f'mkdir -p {"/".join(path.split("/")[:-1])}')

        with open(path, "wb") as f:
            f.write(response.content)

    except Exception as ex:
        session.query(Files).update({
            Files.status: Files.STATUS_FAIL,
            Files.error: str(ex)
        })
        session.commit()

    else:
        session.query(Files).update({Files.status: Files.STATUS_COMPLETE})
        session.commit()
    checked_id.remove(file.id)


def worker():
    while True:
        file = files_queue.get()
        download_file(file)


def start(worker_counter: int = int(os.getenv('WORKER_COUNTER'))):
    workers = []
    for _ in range(worker_counter):
        worker_thread = threading.Thread(target=worker)
        workers.append(worker)
        worker_thread.start()

    while True:
        time.sleep(1)
        for file in session.query(Files).filter(
                Files.status == Files.STATUS_NEW,
                Files.id.notin_(checked_id)
        ).all():
            files_queue.put(file)
            checked_id.append(file.id)


if __name__ == '__main__':
    start()
