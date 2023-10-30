import logging
import time
import click
from rich.logging import RichHandler

from mango_server.config import application_conf


# Logging stuff
def get_rich_logger():
    log_level = application_conf.get('log_level')

    if not log_level:
        log_level = "INFO"

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
    )
    new_logger = logging.getLogger("rich")

    return new_logger


logger = get_rich_logger()


# Timer
def timer_util(func):
    def wrapper(*args, **kwargs):
        # Start timer
        start_time = time.time()
        # Run function
        _ = func(*args, **kwargs)
        # End timer
        end_time = time.time()
        logger.debug(f"Time elapsed: {end_time - start_time} seconds")

    return wrapper
