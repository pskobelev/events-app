import logging


def configure_logging(level=logging.DEBUG):
    logging.basicConfig(
        # datefmt='%Y-%m-%d %H:%M:%S',
        format="[%(asctime)s]%(levelname)6s | %(module)s:%(lineno)d > %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(level=level)

    return logger
