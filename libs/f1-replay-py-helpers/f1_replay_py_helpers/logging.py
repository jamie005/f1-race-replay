import colorlog


color_log_handler = colorlog.StreamHandler()
color_log_handler.setFormatter(colorlog.ColoredFormatter(
    '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s.%(filename)s:%(lineno)d%(reset)s %(message)s'))
