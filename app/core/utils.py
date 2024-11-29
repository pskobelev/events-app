import logging
import sys
from app.core.config import get_config

config = get_config()


def setup_logging(cfg) -> None:
    logging_level = logging.DEBUG if cfg.DEBUG else logging.INFO
    logging.basicConfig(level=logging_level, stream=sys.stdout)
