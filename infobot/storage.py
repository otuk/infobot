# import infobot.konstants


class Admin():

    def __init__(self, config):
        "abstract"
        self.config = config
        pass

    def store(self, data):
        raise NotImplementedError()

    def read(self, data):
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

    def read(self):
        print("file admin ", self._directory)
        # with open(filename) as conf:
        #    pass
