import yaml


class Topic():
    def __init__(self, filedata):
        "docstring"
        self.name = filedata["name"]
        self.storagemodule = filedata["storagemodule"]
        self.storageclass = filedata["storageclass"]
        self.socialmodule = filedata["socialmodule"]
        self.socialclass = filedata["socialclass"]
        # sample optional argument
        # self.opt = filedata.get("opt", "")


class Randomizer():
    def __init__(self, filedata):
        "docstring"
        self.ontimes = int(filedata["ontimes"])
        self.outoftimes = int(filedata["outoftimes"])
        self.start = int(filedata["start"])
        excludeList = filedata["exclude"].split(",")
        self.exclude = [int(i) for i in excludeList]


class Admin():
    def __init__(self, filepath):
        "docstring"
        filedata = Admin.read_yaml(filepath)
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
