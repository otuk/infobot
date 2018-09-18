import os

# import infobot.konstants
from infobot.storage.template import Admin
from infobot.config import Admin as ConfigAdm
from infobot.brains import Brains


class FileAdminConf():
    def __init__(self, filedata):
        "docstring"
        self.directory = Brains.expand_home(
            filedata["directory"])
        self.indexfile = Brains.expand_home(
            filedata["indexfile"])


class FileAdmin(Admin):
    def __init__(self, config, fileadmindetails):
        "docstring"
        super().__init__(config)
        self._details = FileAdminConf(fileadmindetails)
        self._directory = self._details.directory
        self._indexfile = self._details.indexfile

    def format_index(self, topicName, num):
        return topicName + "_" + str(num) + ".txt"

    def read_from(self, index):
        fullpath = os.path.join(self._directory, index)
        with open(fullpath) as postfile:
            postdata = postfile.read()
        return postdata

    def get_index(self):
        indexData = ConfigAdm.read_yaml(self._indexfile)
        return (int(indexData["start"]),
                int(indexData["last"]),
                int(indexData["previous"]))

    def get_header(self, socialnetwork, topic, num):
        return """
{}:{}
-----------------------

    """.format(topic, num)

    def get_footer(self, socialnetwork, topic, num):
        return """
-----------------------
for correction requests please include: {}:{}
    """.format(topic, num)
