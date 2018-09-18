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
    def __init__(self, config, socialplugindetails, storageadmin):
        "docstring"
        super().__init__(config)
        self._details = FakeSocialPluginConf(socialplugindetails)
        self._userid = self._details.userid
        self._password = self._details.password
        self.storageAdmin = storageadmin

    def login(self):
        return True

    def logout(self):
        return True

    def post(self, num, data):
        print(data)
        print("corrections send to ", num)

    def list_followers(self):
        return["a", "b", "c"]

    def follow(self, other):
        print("following @"+other)
