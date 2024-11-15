import logging

logger = logging.getLogger(__name__)


if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())
