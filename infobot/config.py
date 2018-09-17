import yaml


class Topic():
    def __init__(self, filedata):
        "docstring"
        self.name = filedata["name"]
        self.storageclass = filedata["storageclass"]
        self.socialclass = filedata["socialclass"]
        self.opt = filedata.get("opt", "")  # how to handle an optional field


class Randomizer():
    def __init__(self, filedata):
        "docstring"
        self.ontimes = int(filedata["ontimes"])
        self.outoftimes = int(filedata["outoftimes"])
        self.start = int(filedata["start"])
        excludeList = filedata["exclude"].split(",")
        self.exclude = [int(i) for i in excludeList]


class Admin():
    def __init__(self, filedata):
        "docstring"
        self.topic = Topic(filedata["topic"])
        self.randomizer = Randomizer(filedata["randomizer"])
        self.storageadmindetails = filedata[self.topic.storageclass
                                            + "Details"]
        self.socialplugindetails = filedata[self.topic.socialclass
                                            + "Details"]

    @staticmethod
    def read_yaml(yamlFilePath):
        with open(yamlFilePath) as yf:
            data = yaml.safe_load(yf.read())
        return data
