import datetime
import logging
import os


class SingletonLogger(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonLogger, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyLogger(object, metaclass=SingletonLogger):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.NOTSET)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()
        dirname = "./log"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        file_handler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")

        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)

    def get_logger(self):
        return self._logger


def get_logger():
    return MyLogger.__call__().get_logger()
