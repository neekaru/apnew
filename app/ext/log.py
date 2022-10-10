from app import app
from logging import basicConfig, getLogger, FileHandler, StreamHandler, DEBUG, error as log_error, info as log_info, warning as log_warning

logger = getLogger('werkzeug')
handler = FileHandler('test.log')
logger.addHandler(handler)

# basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     handlers=[FileHandler('log.txt'), StreamHandler()],
#                     level=DEBUG)

def error(reason):
    return logger.error(reason)

def info(reason):
    return logger.info(reason)

def warning(reason):
    return logger.warning(reason)

def debug(reason):
    return logger.debug(reason)