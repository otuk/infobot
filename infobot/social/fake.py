import os

# import infobot.konstants
from infobot.config import Admin as ConfigAdm


class SocialPlugin():
    def __init__(self, config):
        "abstract"
        self.config = config
        pass

    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def post(self, data):
        raise NotImplementedError()

    def list_followers(self):
        raise NotImplementedError()

    def follow(self, other):
        raise NotImplementedError()


class FakeSocialPluginConf():
    def __init__(self, filedata):
        "docstring"
        self.userid = filedata["userid"]
        self.password = filedata["password"]


class FakeSocialPlugin(SocialPlugin):
    def __init__(self, config, socialplugindetails):
        "docstring"
        super().__init__(config)
        self._details = FakeSocialPluginConf(socialplugindetails)
        self._userid = self._details.directory
        self._password = self._details.indexfile

    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def post(self, data):
        raise NotImplementedError()

    def list_followers(self):
        raise NotImplementedError()

    def follow(self, other):
        raise NotImplementedError()
