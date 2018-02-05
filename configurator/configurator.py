import json
import os

from loader.loader import FileLoader


class AlertConf:
    def __init__(self, file_path):
        self.path = file_path
        self.host_name = os.path.split(os.path.split(file_path)[0])[1]
        self.measurement = os.path.splitext(os.path.basename(file_path))[0]
        self.base_path = os.path.dirname(file_path)

    def getConfigurationList(self):
        data = FileLoader(self.path).getData()
        result = dict()
        for i in data['instance']:
            o_data = dict()
            database = {"database": {"type": "string", "value": data['database']}}
            host = {"host": {"type": "string", "value": self.host_name}}
            instance = {"instance": {"type": "string", "value": self.checkIsNil(i['name'])}}
            type = {"type": {"type": "string", "value": self.checkIsNil(i['type'])}}
            type_instance = {"type_instance": {"type": "string", "value": self.checkIsNil(i['type_instance'])}}
            # template = {"template": {"type": "string", "value": i['template']}}
            alet_conf = self.checkIsNil(i['alet_conf'])
            o_data.update(database)
            o_data.update(host)
            o_data.update(instance)
            o_data.update(type)
            o_data.update(type_instance)
            # o_data.update(template)
            o_data.update(alet_conf)
            o_data.update(self.get_mail_conf())
            file_name = self.generate_file_name({'host': self.host_name,
                                                 'measurement': self.measurement,
                                                 'name': i['name'],
                                                 'type': i['type'],
                                                 'type_instance': i['type_instance'],
                                                 'template': i['template']})

            result.update({file_name: o_data})
        return result

    def generate_file_name(self, atr):
        for key, value in atr.items():
            if self.checkIsNil(value) == "":
                atr[key] = "NIL"
        result = """{host}_{measurement}_{name}_{type}_{type_instance}__{template}""".format(host=atr['host'],
                                                                                             measurement=atr['measurement'],
                                                                                            name=atr['name'],
                                                                                            type=atr['type'],
                                                                                            type_instance=atr['type_instance'],
                                                                                            template=atr['template']
                                                                                            )
        return result

    def checkIsNil(self, value):
        if value == "nil" or value == "null" or value is None:
            return ""
        else:
            return value

    def get_email_data(self, path):
        data = FileLoader(path).getData()
        return data

    def get_mail_conf(self):
        email_file_name = "email_channel.yaml"
        base_email_file_path = os.path.join(os.path.dirname(self.base_path), email_file_name)
        override_email_path = os.path.join(self.base_path, email_file_name)
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
