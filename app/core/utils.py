import logging


def configure_logging(
        level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s %(name)-12s [%(levelname)-7s]-[:%(lineno)d] - %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(level=level)

    return logger