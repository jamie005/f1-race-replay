from logging import Logger 

import colorlog


def configure_logger(logger: Logger, log_level: str) -> None:
    logger.setLevel(log_level)  
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
	    '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s.%(filename)s:%(lineno)d%(reset)s %(message)s'))
    logger.addHandler(handler)
