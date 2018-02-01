import json
import os

from bin.loader.loader import FileLoader

class AlertConf:

    def __init__(self, file_path):
       self.path = file_path
       self.host_name = os.path.split(os.path.split(file_path)[0])[1]
       self.measurment = os.path.splitext(os.path.basename(file_path))[0]
       self.base_path = os.path.dirname(file_path)

    def getConfigurationList(self):
        data = FileLoader(self.path).getData()
        result = dict ()

        for i in data['instance']:
            o_data = dict()
            instance = {"instance" : { "type" : "string","value" : self.checkIsNil(i['name'])}}
            type =  {"type" : { "type" : "string","value" : self.checkIsNil(i['type'])}}
            type_instance ={"type_instance" : { "type" : "string","value" : self.checkIsNil(i['type_instance']['name'])}}
            template = {"template" : { "type" : "string","value" : i['template']}}
            alet_conf = i['type_instance']['alet_conf']
            o_data.update(instance)
            o_data.update(type)
            o_data.update(type_instance)
            o_data.update(template)
            o_data.update(alet_conf)
            file_name = self.host_name + "_" \
                        + self.measurment + "_" \
                        + i['name'] + "_" + i['type'] + "_" \
                        + i['type_instance']['name']
            result.update({ file_name : o_data})
        return result

    def checkIsNil(self, value):
        if value == "nil":
            return ""
        else:
            return value

    def generate_alerts_conf(self):
        data_to_save = self.getConfigurationList()
        output_dir = os.path.join(self.base_path,"output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for key, value in data_to_save.items():
            output_path = os.path.join(output_dir,key + ".json")
            self.write_conf_to_file(output_path,value)

    def write_conf_to_file(self, path, data):
        with open(path, 'w') as outfile:
            json.dump(data, outfile,indent=4)



