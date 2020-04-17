from queue import Queue
from threading import Thread


class ThreadManager(object):

    # Main background worker - wrapper of function
    def _worker(self):
        while True:
            try:
                # get one function with arguments from queue
                func, args, kwargs = self._threads.get()
                # and execute it
                func(*args, **kwargs)
            except Exception as e:
                print("Exception: " + str(e))
            self._threads.task_done()

    def __init__(self, thread_count):
        """
        Constructor for ThreadManager class
        :param thread_count: Maximal capacity of threads queue
        """
        self._thread_count = thread_count
        self._threads = Queue(maxsize=self._thread_count)
        for _ in range(self._thread_count):
            worker_thread = Thread(target=self._worker)
            worker_thread.setDaemon(True)
            worker_thread.start()

    def add_task(self, func, *args, **kwargs):
        """
        Add task to queue for background working
        :param func: Target function for executing
        :param args: Positional arguments of function
        :param kwargs: Keyword arguments of function
        :return: None
        """
        self._threads.put((func, args, kwargs,))

    def wait_for_completion(self):
        """
        Sync all threads
        :return: None
        """
        self._threads.join()