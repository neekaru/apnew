from api_app import app
from logging import DEBUG, FileHandler, DEBUG, error as log_error, info as log_info, warning as log_warning

handler = FileHandler('test.log')
app.logger.addHandler(handler)
app.logger.setLevel(DEBUG)
# basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     handlers=[FileHandler('log.txt'), StreamHandler()],
#                     level=DEBUG)

def error(reason):
    return app.logger.error(reason)

def info(reason):
    return app.logger.info(reason)

def warning(reason):
    return app.logger.warning(reason)

def debug(reason):
    return app.logger.debug(reason)