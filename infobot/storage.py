import os

# import infobot.konstants
from infobot.config import Admin as ConfigAdm


class Admin():
    def __init__(self, config):
        "abstract"
        self.config = config
        pass

    def store(self, data):
        raise NotImplementedError()

    def read(self, data):
        raise NotImplementedError()

    def get_index(self):
        raise NotImplementedError()


class FileAdminConf():
    def __init__(self, filedata):
        "docstring"
        self.directory = filedata["directory"]
        self.indexfile = filedata["indexfile"]


class FileAdmin(Admin):
    def __init__(self, config, fileadmindetails):
        "docstring"
        super().__init__(config)
        self._details = FileAdminConf(fileadmindetails)
        self._directory = self._details.directory
        self._indexfile = self._details.indexfile

    def read(self, filename):
        fullpath = os.path.join(self._directory, filename + ".txt")
        print("file admin ", self._directory)
        with open(fullpath) as postfile:
            postdata = postfile.read()
        print(postdata)
        return postdata

    def get_index(self):
        indexData = ConfigAdm.read_yaml(self._indexfile)
        return (int(indexData["start"]),
                int(indexData["last"]),
                int(indexData["previous"]))
