import logging


class Logging(object):
    def __init__(self, name, level="WARNING", filename=None, mode="a"):
        self.LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
        self.log_datefmt = '%Y-%m-%d %H:%M:%S'
        self.logger = logging.getLogger(name)
        if not isinstance(level, int):
            try:
                level = getattr(logging, level)
            except AttributeError:
                raise ValueError("unsupported literal log level: %s" % level)
            self.logger.setLevel(level)
        if filename:
            self.handler = logging.FileHandler(filename, mode=mode)
        else:
            self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(self.log_format, datefmt=self.log_datefmt)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def get_logger(self):
        return self.logger
