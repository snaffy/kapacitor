import json
import os

from loader.loader import FileLoader


class AlertConf:
    def __init__(self, file_path):
        self.path = file_path
        self.host_name = os.path.split(os.path.split(file_path)[0])[1]
        self.measurment = os.path.splitext(os.path.basename(file_path))[0]
        self.base_path = os.path.dirname(file_path)

    def getConfigurationList(self):
        data = FileLoader(self.path).getData()
        result = dict()
        # data2 = self.check_if_email_is_override()
        for i in data['instance']:
            o_data = dict()
            instance = {"instance": {"type": "string", "value": self.checkIsNil(i['name'])}}
            type = {"type": {"type": "string", "value": self.checkIsNil(i['type'])}}
            type_instance = {"type_instance": {"type": "string", "value": self.checkIsNil(i['type_instance'])}}
            template = {"template": {"type": "string", "value": i['template']}}
            alet_conf = i['alet_conf']
            o_data.update(instance)
            o_data.update(type)
            o_data.update(type_instance)
            # o_data.update(template)
            o_data.update(alet_conf)
            o_data.update(self.get_mail_conf())
            file_name = self.host_name + "_" \
                        + self.measurment + "_" \
                        + i['name'] + "_" + i['type'] + "_" \
                        + i['type_instance'] + "__" + i['template']
            result.update({file_name: o_data})
        return result

    def checkIsNil(self, value):
        if value == "nil":
            return ""
        else:
            return value

    def get_email_data(self, path):
        data = FileLoader(path).getData()
        return data

    def get_mail_conf(self):
        email_file_name = "email_channel.yaml"
        base_email_file_path = os.path.join(os.path.dirname(self.base_path), email_file_name)
        override_email_path = os.path.join(self.base_path,email_file_name)
        if os.path.isfile(override_email_path):
            o_data = dict()
            d1 = self.get_email_data(override_email_path)
            d2 = self.get_email_data(base_email_file_path)
            d3 = d1.get('email_channel')['value'] + d2.get('email_channel')['value']
            o_data.update({'email_channel': {'type': 'list', 'value': d3}})
            return o_data
        else:
            return self.get_email_data(base_email_file_path)


    def generate_alerts_conf(self):
        data_to_save = self.getConfigurationList()
        output_dir = os.path.join(self.base_path, "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for key, value in data_to_save.items():
            output_path = os.path.join(output_dir, key + ".json")
            self.write_conf_to_file(output_path, value)

    def write_conf_to_file(self, path, data):
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4)
