import logging
import os
from datetime import date


class ReaLogger:

    def __init__(self, name):
        filename = os.environ['REA_DATA'] + '/logs/rea_' + date.today().strftime('%Y_%m_%d') + '.log'
        # logging.basicConfig(filename=filename, level=logging.WARN)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter('%(asctime)s : %(message)s', '%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(filename, mode='w')
        file_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)

    def output_console(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

