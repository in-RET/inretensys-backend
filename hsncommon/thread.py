import threading
import atexit
import time
import uuid

from .log import HsnLogger
log = HsnLogger()

class HsnBackgroundThreadHandler(object):
    __threads = None
    __stop_event = None

    
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        self.__threads = dict()
        self.__stop_event = threading.Event()
        atexit.register(self.__kill_all_background_threads)


    def start_background_task(self, worker, *args, **kwargs):
        uid = uuid.uuid4().hex

        def __call():
            worker(self.__stop_event, *args, **kwargs)

        self.__threads[uid] = threading.Thread(name=uid, target=__call)
        self.__threads[uid].start()

        return uid

    def __kill_all_background_threads(self):
        self.__stop_event.set()
        time.sleep(1)
        for key in self.__threads:
            self.__threads[key].join()
