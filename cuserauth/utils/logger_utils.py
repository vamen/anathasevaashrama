import logging

def init_logger():
    logger = logging.getLogger("MAIN")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.error("logging data")
    logger.debug("logging debug")
    logger.info("logging info")
    return logger
# TODO : ABHI