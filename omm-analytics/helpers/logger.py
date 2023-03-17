import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import dotenv_values

config = dotenv_values(".env")
log_file = config.get("log_file")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(log_file,
                                   when="d",
                                   interval=1,
                                   backupCount=7)

fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
formatter = logging.Formatter(fmt=fmt, datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)
logger.addHandler(console)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.addHandler(handler)