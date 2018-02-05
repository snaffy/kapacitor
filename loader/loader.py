import yaml
import logging


class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def getData(self):
        with open(self.file_path) as stream:
            try:
                tmp = (yaml.safe_load(stream))
                if tmp is None:
                    raise Exception('There was a problem during loading the configuration file')
                return tmp
            except Exception as exc:
                logging.error(self.file_path)
                logging.error(exc)
                exit(1)

