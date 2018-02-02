import os


class ProjectConf:
    main_conf_dir_name = 'main-config'
    template_dir_name = 'templates'

    @staticmethod
    def get_base_path():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_default_template_dir_path():
        return os.path.join(os.path.dirname(ProjectConf.get_base_path()), ProjectConf.template_dir_name, '')

    @staticmethod
    def get_main_config_path():
        return os.path.join(os.path.dirname(ProjectConf.get_base_path()), ProjectConf.main_conf_dir_name, '')

