import abc

import os


class Task(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self):
        pass

class TaskManager(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.path = path

    @abc.abstractmethod
    def create(self):
        pass


    def get_task_list(self):
        task_list = list()
        if os.path.exists(self.path):
            for entry in os.listdir(self.path):
                task_list.append(os.path.join(self.path, entry))
        return task_list