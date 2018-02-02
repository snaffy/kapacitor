import os
from pip import logger

from execution.executor import Executor
from projectconfiguration import ProjectConf

print(ProjectConf.get_default_template_dir_path())


class TemplateManager:
    default_templates_dir_path = ProjectConf.get_default_template_dir_path()

    def get_template_list(self):
        template_conf_list = list()
        if os.path.exists(self.default_templates_dir_path):
            for entry in os.listdir(self.default_templates_dir_path):
                template_conf_list.append(os.path.join(self.default_templates_dir_path, entry))
        return template_conf_list

    def create_templates(self):
        for item in self.get_template_list():
            Template(item).create()


class Template:
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


x = TemplateManager()
print(x.create_templates())
