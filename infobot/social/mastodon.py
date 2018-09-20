from mastodon import Mastodon

import infobot.konstants as K
from infobot.social.template import SocialPlugin


# Log in - either every time, or use persisted
"""
"""


class MastodonPluginConf():
    def __init__(self, filedata):
        "Handles the configuation data for Mastodon plugin"
        self.socialAppName = filedata[K.socialAppKey]
        self.clientAppName = filedata[K.clientAppNameKey]
        self.apiURL = filedata[K.apiURLKey]
        self.clientSecretFilename = filedata[K.clientSecretKey]
        self.userSecretFilename = filedata[K.userSecretKey]


class MastodonPlugin(SocialPlugin):
    def __init__(self, config, socialplugindetails, storageadmin):
        """
        This is a reference class for a social plugin
        It does not post to any social network
        It simply outputs to the stdout as if it is posting
        """
        details = MastodonPluginConf(socialplugindetails)
        super().__init__(config, details.socialAppName)
        self._details = details
        self._clientappname = self._details.clientAppName
        self._apiURL = self._details.apiURL
        self._clientSecretFilename = self._details.clientSecretFilename
        self._userSecretFilename = self._details.userSecretFilename
        self.storageAdmin = storageadmin

    def register(self):
        # Register app - only once!
        Mastodon.create_app(
            self._clientappname,
            api_base_url=self._apiURL,
            to_file=self._clientSecretFilename
        )
        # this also logs in making the app ready for posting
        self.login()

    def login(self):
        # login and save login key
        mastodon = Mastodon(
            client_id=self._clientSecretFilename,
            api_base_url=self._apiURL
        )
        uid = str(input("Enter mastodon userid email (e.g abc@xyz.com): "))
        pwd = input("Enter password for user {}: ".format(uid))
        mastodon.log_in(
            uid,
            pwd,
            to_file=self._userSecretFilename
        )

    def logout(self):
        print("Logging out from mastodon.")
        return True

    def registered(self):
        return False

    def post(self, topic, num, data):
        if not self.registered():
            print(
                ("{} requires a one time registration, "
                 "please run with '-r' flag first").format(
                    self.socialName))
            return False
        hdr = self.storageAdmin.get_header(self.socialName, topic, num)
        ftr = self.storageAdmin.get_footer(self.socialName, topic, num)
        postdata = "{}\n{}\n{}".format(hdr, data, ftr)
        # Create actual API instance
        mastodon = Mastodon(
            access_token=self._userSecretFilename,
            api_base_url=self._apiURL
        )
        mastodon.toot(postdata)
        return True

    def list_followers(self):
        return["a", "b", "c"]

    def follow(self, other):
        print("following @"+other)
