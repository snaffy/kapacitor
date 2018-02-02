import os
from pip import logger
from execution.executor import ExecuteCommand, Executor


class TaskManager:
    output_dir_name = "output"

    def __init__(self, alerts_dir_conf_path):
        self.alerts_dir_conf_path = alerts_dir_conf_path
        self.output_path = os.path.join(self.alerts_dir_conf_path, self.output_dir_name)

    def get_task_list(self):
        alet_conf_list = list()
        if os.path.exists(self.output_path):
            for entry in os.listdir(self.output_path):
                alet_conf_list.append(os.path.join(self.output_path,entry))
        return alet_conf_list

    def create_alerts(self):
        for item in self.get_task_list():
            Task(item).create()


class Task:
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


conf_path = "C:\\Projects\\monitoring_root\\monitoring_client\\rva\\kapacitor\\vehicle-event-router-staging-yaml-concept-flat-structure\\output\\vehicle-event-router-staging-yaml-concept-flat-structure_dbi_value_events_gauge_event_archiving__progress_template.json"
alert_path = "C:\\Projects\\monitoring_root\\monitoring_client\\rva\\kapacitor\\vehicle-event-router-staging-yaml-concept-flat-structure"

x = TaskManager(alert_path)
# list = x.get_task_list()
# print(list)
x.create_alerts()
