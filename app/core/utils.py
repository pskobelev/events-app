import logging


def configure_logging(level=logging.DEBUG):
    logging.basicConfig(
        # format="%(asctime)s [%(name)s:%(lineno)10d] [%(levelname)-7s] > %(message)s"
        # format='%(asctime)s [%(levelname)-7s] - %(name)s > %(message)s'
        datefmt='%Y-%m-%d %H:%M:%S',
        format="[%(asctime)s] %(module)s.%(funcName)s:%(lineno)d %(levelname)-7s>> %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(level=level)

    return logger
