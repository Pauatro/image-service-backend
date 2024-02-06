import logging
from shared.settings import Settings

settings = Settings()
Logger = logging.Logger

def get_logger():
    return logging.getLogger(settings.logger)