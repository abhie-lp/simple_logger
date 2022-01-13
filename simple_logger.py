from logging import getLogger, Logger, Formatter, StreamHandler, \
    DEBUG, INFO, ERROR, WARNING, CRITICAL
from os import makedirs, path
from logging.handlers import TimedRotatingFileHandler


FORMATTER = Formatter(
    '%(asctime)s [%(levelname)s][%(module)s][%(lineno)d] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)


def create_logger(name: str, filename: str, log_level: int = INFO) -> Logger:
    """
    Create and return the Logger object
    :param name: name of the logger
    :param filename: path where logs will be stored
    :param log_level: Level of logging. By default INFO is set
    :return: Logger
    """

    assert log_level in (DEBUG, INFO, ERROR, WARNING, CRITICAL), f'{log_level} is an invalid level'

    # Add .log at the end of the filename if not present
    if not filename.endswith('.log'):
        filename += '.log'

    # Check if filename is in some directory
    if path.dirname(filename):
        if not path.exists(path.dirname(filename)):
            # Create directory if it does not exist
            makedirs(path.dirname(filename), exist_ok=True)

    logger = getLogger(name)
    logger.setLevel(log_level)

    file_handler = TimedRotatingFileHandler(filename, when='midnight', backupCount=15)
    stream_handler = StreamHandler()

    # Append .log at the end of rotated file
    file_handler.namer = lambda log_filename: log_filename.replace('.log', '') + '.log'
    file_handler.setFormatter(FORMATTER)
    stream_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
