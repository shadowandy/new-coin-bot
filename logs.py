import logging
import sys
import os

from config.config import config

__all__ = ('logger', )

def get_logger():
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%b-%y %H:%M:%S')
    _logger = logging.getLogger()
    if config.console_logs:
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        _logger.addHandler(screen_handler)
        _logger.setLevel(logging.NOTSET)
    if config.logs_file is not None:
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.logs_file)
        handler = logging.FileHandler(file_name, mode='a')
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(logging.NOTSET)
    return _logger


logger = get_logger()
