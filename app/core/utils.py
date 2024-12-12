import logging


def configure_logging(
        level=logging.INFO):
    logging.basicConfig(
        # format="%(asctime)s [%(name)s:%(lineno)10d] [%(levelname)-7s] > %(message)s"
        # format='%(asctime)s [%(levelname)-7s] - %(name)s > %(message)s'
        format='%(asctime)s [%(levelname)-7s] - [%(filename)s).%(funcName)s(%(lineno)d)] > %(message)s'
    )
    logger = logging.getLogger()
    logger.setLevel(level=level)

    return logger