from subprocess import call


class ExecuteCommand:
    def __init__(self, command, expect=None):
        self.command = command
        self.expect = expect


class Executor:
    def __init__(self):
        pass

    @staticmethod
    def execute_commands_list(commands_list):
        for execute_command in commands_list:

            result_code = Executor.execute_cmd_command(execute_command)

            if result_code != 0:
                return result_code

        return 0

    @staticmethod
    def execute_cmd_command(execute_command):
        result_code = call(execute_command, shell=True)
        if result_code != 0:
            return result_code


