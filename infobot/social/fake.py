# import infobot.konstants


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
        "Handles the configuation data for social plugin"
        self.userid = filedata["userid"]
        self.password = filedata["password"]


class FakeSocialPlugin(SocialPlugin):
    def __init__(self, config, socialplugindetails, storageadmin):
        """
        This is a reference class for a social plugin
        It does not post to any social network
        It simply outputs to the stdout as if it is posting
        """
        super().__init__(config)
        self._details = FakeSocialPluginConf(socialplugindetails)
        self._userid = self._details.userid
        self._password = self._details.password
        self.storageAdmin = storageadmin

    def login(self):
        print("Logging into fake with {}/{}".
              format(self._userid, self._password))
        return True

    def logout(self):
        print("Logging out from fake.")
        return True

    def post(self, topic, num, data):
        hdr = self.storageAdmin.get_header("fake", topic, num)
        ftr = self.storageAdmin.get_footer("fake", topic, num)
        postdata = "{}\n{}\n{}".format(hdr, data, ftr)
        print(postdata)
        return postdata

    def list_followers(self):
        return["a", "b", "c"]

    def follow(self, other):
        print("following @"+other)
