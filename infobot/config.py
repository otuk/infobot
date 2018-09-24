import yaml


class Topic():
    def __init__(self, filedata):
        """
        Simple configuration file helper: Topic details
        """
        self.name = filedata["name"]


class Randomizer():
    def __init__(self, filedata):
        """
        Simple configuration file helper: Random posting behavior control
        """
        self.ontimes = int(filedata["ontimes"])
        self.outoftimes = int(filedata["outoftimes"])
        self.start = int(filedata["start"])
        excludeList = filedata["exclude"].split(",")
        self.exclude = [int(i) for i in excludeList]


class Dev():
    def __init__(self, filedata):
        """
        Only for developers
        Use this configuration helper to extend infobot
        """
        self.storagemodule = filedata["storagemodule"]
        self.storageclass = filedata["storageclass"]
        self.socialmodule = filedata["socialmodule"]
        self.socialclass = filedata["socialclass"]
        # sample optional argument
        # self.opt = filedata.get("opt", "")


class Admin():
    def __init__(self, filepath):
        """
        This is the main configuration admin class.
        It parses the  configuration from a yaml file.
        The file name is given as a commandline argument to the prog.
        """
        filedata = Admin.read_yaml(filepath)
        self.configfilepath = filepath
        self.topic = Topic(filedata["topic"])
        self.dev = Dev(filedata["dev"])
        self.randomizer = Randomizer(filedata["randomizer"])
        self.storageadmindetails = filedata[self.dev.storageclass
                                            + "Details"]
        self.socialplugindetails = filedata[self.dev.socialclass
                                            + "Details"]

    def status(self):
        print("Infobot instance for topic: {}".format(self.topic.name))
        print("  Configuration file: {}".format(self.configfilepath))
        print("  Posts {} out of {} times".format(
            self.randomizer.ontimes,
            self.randomizer.outoftimes
        ))
        print("  Starting from: {} and excluding: {}".format(
            self.randomizer.start,
            self.randomizer.exclude
        ))

    @staticmethod
    def read_yaml(yamlFilePath):
        with open(yamlFilePath) as yf:
            data = yaml.safe_load(yf.read())
        return data
