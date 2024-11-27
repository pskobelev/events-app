import logging
import sys
from app.config import get_config

config = get_config()


def setup_logging(config: config) -> None:
    logging_level = logging.DEBUG if config.DEBUG else logging.INFO
    logging.basicConfig(level=logging_level, stream=sys.stdout)
