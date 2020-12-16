from datetime import datetime
# from logbook import FileHandler, RotatingFileHandler, Logger, DEBUG, ERROR, INFO, WARNING, TRACE
import logging
from logging import Logger, DEBUG, ERROR, INFO, WARNING, CRITICAL


class SimsLogging:
    logger = None

    def __init__(self, logger_name, logger_level=DEBUG, rotate_logs=False):
        tmp_date_string = datetime.now().isoformat().replace("T", "_").replace("-", "").replace(":", "")
        tmp_file_name = "simsUnzipper_{}.log".format(tmp_date_string)
        out_file_name = "simsUnzipper.log" if rotate_logs else tmp_file_name
        logging.basicConfig(filename=out_file_name, level=DEBUG, format="%(asctime)s %(message)s")
        if self.logger is None:
            self.logger = logging.getLogger(logger_name)

    def warn(self, message):
        """
        Provided as a convenience for those that got used to this as the method name
        :param message: message to write to the log file
        :return:
        """
        self.logger.warning(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def trace(self, message):
        """
        Provided as a convenience for those that got used to this as the method name
        :param message: message to write to the log file
        :return:
        """
        self.logger.critical(message)

    def critical(self, message):
        self.logger.critical(message)


