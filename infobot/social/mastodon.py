import os
from mastodon import Mastodon

import infobot.konstants as K
from infobot.brains import Brains
from infobot.social.template import SocialPlugin


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
        self._clientSecretFilename = Brains.expand_home(
            self._details.clientSecretFilename)
        self._userSecretFilename = Brains.expand_home(
            self._details.userSecretFilename)
        self.storageAdmin = storageadmin

    def status(self):
        print("Mastodon social plugin is active with appname {}".format(
            self._clientappname
        ))
        print("  This client is registered: {}".format(self.registered()))
        print("  This user is logged in: {}".format(self.logged_in()))

    def register(self):
        # Register app - only once!
        Mastodon.create_app(
            self._clientappname,
            api_base_url=self._apiURL,
            to_file=self._clientSecretFilename
        )
        # this also logs in making the app ready for posting
        if self.login():
            if self.logged_in():
                print("One time registration succesfully completed")
                return True
        else:
            return False

    def login(self):
        if not self.registered():
            print(
                ("{} requires a one time registration, "
                 "please run with '-r' flag first").format(
                    self.socialName))
            return False
        if self.logged_in():
            return True
        # login and save login key
        mastodon = Mastodon(
            client_id=self._clientSecretFilename,
            api_base_url=self._apiURL
        )
        uid = str(input("Enter mastodon userid email (e.g abc@xyz.com): "))
        pwd = str(input("Enter password for user {}: ".format(uid)))
        mastodon.log_in(
            uid,
            pwd,
            to_file=self._userSecretFilename
        )
        return True

    def logout(self):
        pass

    def registered(self):
        # ensure client secret file is in place
        # and it is not 0 length
        if os.path.exists(self._clientSecretFilename):
            if os.path.isfile(self._clientSecretFilename):
                if os.path.getsize(self._clientSecretFilename) > 0:
                    return True
        return False

    def logged_in(self):
        # ensure user secret file is in place
        # and it is not 0 length
        if os.path.exists(self._userSecretFilename):
            if os.path.isfile(self._userSecretFilename):
                if os.path.getsize(self._userSecretFilename) > 0:
                    return True
        return False

    def post(self, topic, num, data):
        if not self.logged_in():
            self.login()
            if not self.logged_in():
                assert(False)
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
