import yaml


class Topic():
    def __init__(self, filedata):
        "docstring"
        self.name = filedata["name"]


class Storage():
    def __init__(self, filedata):
        "docstring"
        self.directory = filedata["directory"]


class Admin():
    def __init__(self, filedata):
        "docstring"
        self.topic = Topic(filedata["topic"])
        self.storage = Storage(filedata["storage"])

    @classmethod
    def readYaml(yamlFilePath):
        with open(yamlFilePath) as yf:
            data = yaml.safe_load(yf.read())
        return data
