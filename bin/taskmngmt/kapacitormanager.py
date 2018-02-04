import os

from pip import logger
from execution.executor import ExecuteCommand, Executor
from taskmngmt.manager import Task, TaskManager


class KapacitorTaskManager(TaskManager):
    output_dir_name = "output"

    def __init__(self, alerts_dir_conf_path):
        self.output_path = os.path.join(alerts_dir_conf_path, self.output_dir_name)
        super().__init__(self.output_path)

    def create(self):
        for item in self.get_task_list():
            KapacitorTask(item).create()

class KapacitorTemplateManager(TaskManager):

    def __init__(self, path_to_template_dir):
        super().__init__(path_to_template_dir)

    def create(self):
        for item in self.get_task_list():
            KapacitorTemplate(item).create()


class KapacitorTask(Task):
    def __init__(self, conf_path):
        self.conf_path = conf_path
        # TODO generwoac tez informacje o bazie danych
        self.db_rp = "collectd.autogen"
        self.base_name = os.path.basename(conf_path)
        self.template_name = StringExtractor.between(self.base_name, "__", ".json")
        self.task_name = self.base_name.replace("__" + self.template_name + ".json", "")

    def create(self):
        cmd = """kapacitor define {} -template {} -vars {} -dbrp {}""".format(self.task_name, self.template_name,
                                                                              self.conf_path, self.db_rp)
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
