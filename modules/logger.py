import logging 
import sys
import os


class logger:
    # Class variables defining log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    # Default level set for runtime
    LEVEL = INFO

    def __init__(self, file_handler, name= __name__, console= False):
        '''
        You can create a logger with file logging only 
        or both file logging and stdout output
        '''
        self._logger = logging.getLogger(name)
        self._file_handler = file_handler
        #Print to stdout or not
        self._console = console

    def setLevel(self):
        self._logger.setLevel(self.LEVEL)

    def config(self):
        self._file_handler  = logging.FileHandler(self._file_handler, encoding="utf-8")
        formatter = logging.Formatter(f"%(asctime)s|%(name)s|{os.getpid()}|%(levelname)s|%(message)s")
        self._file_handler.setFormatter(formatter)
        self._logger.addHandler(self._file_handler)
        # add a stream handler if console is True
        if self._console:
            self._logger.addHandler(logging.StreamHandler(sys.stdout))

    @property
    def log(self):
        self.setLevel()
        self.config()
        return self._logger
