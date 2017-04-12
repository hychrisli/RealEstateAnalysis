import logging
import os
from datetime import date


class ReaLogger:

    def __init__(self, name):
        filename = os.environ['REA_DATA'] + '/logs/rea_' + date.today().strftime('%Y_%m_%d') + '.log'
        # logging.basicConfig(filename=filename, level=logging.WARN)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s : %(message)s', '%m-%d %H:%M:%S')
        fileHandler = logging.FileHandler(filename, mode='w')
        fileHandler.setFormatter(formatter)
        # streamHandler = logging.StreamHandler()
        # streamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        # logger.addHandler(streamHandler)

        print(logger.handlers)
