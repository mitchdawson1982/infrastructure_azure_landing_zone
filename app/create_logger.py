import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():

    log_file = os.path.abspath(os.path.join(os.sep, os.getcwd(), 'logs', 'infrastructure_azure_landing_zone.log'))
    # Create an instance for our logger
    logger = logging.getLogger()
    # Set the level to DEBUG
    logger.setLevel(logging.DEBUG)
    # Create the rotating File handler
    fh = RotatingFileHandler(
        os.path.join(os.getcwd(), log_file),
        mode='a', maxBytes=5000000, backupCount=50
    )
    # Set the level to DEBUG
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # Define our input variables
    logger.info('Setting the appropriate input and config file paths')
    # Define our input variables
    logger.info('Initialising input variables')

    return logger