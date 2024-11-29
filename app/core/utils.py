import logging
import sys

from core.config import get_config

configs = get_config()


def setup_logger(name: str = None):
    # Уровень логирования на основе конфигурации
    logging_level = logging.DEBUG if configs.DEBUG else logging.INFO
    # Формат сообщений
    log_format = "%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s"
    formatter = logging.Formatter(log_format)
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    logger.addHandler(console_handler)

    # Чтобы избежать дублирования сообщений
    logger.propagate = False

    return logger


# Global base loger 'app'
_base_logger = setup_logger()


def get_logger():
    """
    Returns the logger instance with __name__
    :return:
    """
    import inspect
    frame = inspect.stack()[1]
    module_name = inspect.getmodule(frame[0]).__name__

    return _base_logger.getChild(module_name)
