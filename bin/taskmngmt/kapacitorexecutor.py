# class KapacitorExecutor:
#
#     @staticmethod
#     def create_alerts(task_name, template_name, conf_path,):
#         cmd = """kapacitor define {} -template {} -vars {} -dbrp {}""".format(task_name, self.template_name,
#                                                                               self.conf_path, self.db_rp)
#         result = Executor().execute_cmd_command(cmd)
#         if result != 0:
#             logger.error("Failure during create an alert: {}".format(self.task_name))
#         else:
#             logger.info("A new alert [ {} ] has been successfully created".format(self.task_name))
