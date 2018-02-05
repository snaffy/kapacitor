import os

from pip import logger
from execution.executor import Executor
from loader.loader import FileLoader
from taskmngmt.manager import Task, TaskManager


class KapacitorTaskCreator(TaskManager):
    output_dir_name = "output"

    def __init__(self, alerts_dir_conf_path):
        self.output_path = os.path.join(alerts_dir_conf_path, self.output_dir_name)
        super(KapacitorTaskCreator, self).__init__(self.output_path)

    def create(self):
        for item in self.get_task_list():
            KapacitorTask(item).create()


class KapacitorTemplateCreator(TaskManager):
    def __init__(self, path_to_template_dir):
        super(KapacitorTemplateCreator, self).__init__(path_to_template_dir)

    def create(self):
        for item in self.get_task_list():
            KapacitorTemplate(item).create()


class KapacitorTaskManager:
    def __init__(self, task_name_to_manage, time_to_enable, time_unit):
        self.time_unit = time_unit
        self.time_to_enable = time_to_enable
        self.task_name_to_manage = task_name_to_manage

    def disable(self):
        disable_task_cmd = """kapacitor disable {}""".format(self.task_name_to_manage)
        print(disable_task_cmd)
        result = Executor.execute_cmd_command(disable_task_cmd)

        if result != 0:
            logger.error("Failure during disable an alert: {}".format(self.task_name_to_manage))
        else:
            logger.info("Alert [ {} ] has been successfully disabled".format(self.task_name_to_manage))

    def enable(self):
        cmd = """kapacitor enable {task} | at now + {time} {time_unit}""".format(task=self.task_name_to_manage,
                                                                                 time=self.time_to_enable,
                                                                                 time_unit=self.time_unit)
        print(cmd)
        result = Executor.execute_cmd_command(cmd)

        if result != 0:
            logger.error("There was a problem with the process of re-enabling the alarms: {}".format(self.task_name_to_manage))
        else:
            logger.info("Alert [ {} ] will be automatically turned on again {} {} ".format(self.task_name_to_manage,
                                                                                           self.time_to_enable,
                                                                                           self.time_unit))


class KapacitorTask(Task):
    def __init__(self, conf_path):
        self.conf_path = conf_path
        # TODO generwoac tez informacje o bazie danych
        self.db_rp = FileLoader(conf_path).getData()['database']['value']
        self.base_name = os.path.basename(conf_path)
        self.template_name = StringExtractor.between(self.base_name, "__", ".json")
        self.task_name = self.base_name.replace("__" + self.template_name + ".json", "")

    def create(self):
        cmd = """kapacitor define {} -template {} -vars {} -dbrp {}""".format(self.task_name, self.template_name,
                                                                              self.conf_path, self.db_rp)
        print(cmd)
        result = Executor().execute_cmd_command(cmd)
        if result != 0:
            logger.error("Failure during create an alert: {}".format(self.task_name))
        else:
            logger.info("A new alert [ {} ] has been successfully created".format(self.task_name))

    def __str__(self):
        return """
        {}  
        {} 
        {} 
        {}""".format(self.db_rp, self.conf_path, self.task_name, self.template_name)


class KapacitorTemplate(Task):
    def __init__(self, template_path, type="batch"):
        self.type = type
        self.template_path = template_path
        self.template_name = os.path.basename(template_path).replace(".tick", "")

    def create(self):
        cmd = """kapacitor define-template {} -tick {} -type {}""".format(self.template_name, self.template_path,
                                                                          self.type)
        print(cmd)
        # result = Executor().execute_cmd_command(cmd)
        # if result != 0:
        #     logger.error("Failure during create a template: {}".format(self.template_name))
        # else:
        #     logger.info("A new alert [ {} ] has been successfully created".format(self.template_name))


class StringExtractor:
    @staticmethod
    def between(self, a, b):
        pos_a = self.find(a)
        if pos_a == -1: return ""
        pos_b = self.rfind(b)
        if pos_b == -1: return ""
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= pos_b: return ""
        return self[adjusted_pos_a:pos_b]
