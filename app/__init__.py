import logging

from . import config

logger = logging.getLogger()
logger.setLevel(config.LOGLEVEL)

