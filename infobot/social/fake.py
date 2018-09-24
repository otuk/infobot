import infobot.konstants as K
from infobot.social.template import SocialPlugin


class FakeSocialPluginConf():
    def __init__(self, filedata):
        "Handles the configuation data for social plugin"
        self.userid = filedata[K.useridKey]
        self.password = filedata[K.passwdKey]
        self.socialAppName = filedata[K.socialAppKey]


class FakeSocialPlugin(SocialPlugin):
    def __init__(self, config, socialplugindetails, storageadmin):
        """
        This is a reference class for a social plugin
        It does not post to any social network
        It simply outputs to the stdout as if it is posting
        """
        details = FakeSocialPluginConf(socialplugindetails)
        super().__init__(config, details.socialAppName)
        self._details = details
        self._userid = self._details.userid
        self._password = self._details.password
        self.storageAdmin = storageadmin

    def status(self):
        print("Fake social Plugin is active")
        print("  This only prints to stdout, nothing else.")

    def register(self):
        print("No need to register")
        return True

    def login(self):
        print("Logging into fake with {}/{}".
              format(self._userid, self._password))
        return True

    def logout(self):
        print("Logging out from fake.")
        return True

    def post(self, topic, num, data):
        hdr = self.storageAdmin.get_header(self.socialName, topic, num)
        ftr = self.storageAdmin.get_footer(self.socialName, topic, num)
        postdata = "{}\n{}\n{}".format(hdr, data, ftr)
        print(postdata)
        return postdata

    def list_followers(self):
        return["a", "b", "c"]

    def follow(self, other):
        print("following @"+other)
