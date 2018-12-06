import argparse
import importlib
import os

import infobot.konstants as K
from infobot.config import Admin as ConfigAdmin
from infobot.index import RandomHelper


class Brains():
    """
    Brains does the main coordination for infobot.
    It works with social plugin and the storage admin
    to make the posts or add more data for future posts
    from a user supplied directory.
    """

    def __init__(self):
        """
        create a coordinator for infobot
        and start him on its tasks based on
        user supplied command line arguments
        """
        args = Brains.process_args()
        configFileName = Brains._get_config_file_name(args)
        self.config = ConfigAdmin(configFileName)
        StorageAdmin = self.resolve_storage_admin()
        self.storageAdmin = StorageAdmin(
            self.config, self.config.storageadmindetails)
        self.randomHelper = RandomHelper(self.config, self.storageAdmin)
        SocialPlugin = self.resolve_social_plugin()
        self.socialPlugin = SocialPlugin(
            self.config, self.config.socialplugindetails, self.storageAdmin)
        self.wakeup(args)

    def wakeup(self, args):
        """
        There are two modes of operations
        Main mode is to wake up and make a post to a social network
        The other one is when future posts are added to a storage destination
        """
        if args.addfrompath is not None:
            self.add_future_posts(args.addfrompath)
        elif args.download:
            self.download_future_posts()
        elif args.liststatus:
            self.display_status()
        elif args.registerapp:
            self.register_app()
        else:
            if self.randomHelper.should_i_run():
                self.post_to_social()

    def display_status(self):
        self.config.status()
        self.storageAdmin.status()
        self.socialPlugin.status()

    def post_to_social(self):
        """
        This is the method that organizes the social network interaction
        """
        num = self.randomHelper.get_random_number()
        index = self.storageAdmin.format_index(
            self.config.topic.name,
            num)
        filedata = self.storageAdmin.read_from(index)
        self.socialPlugin.login()
        self.socialPlugin.post(self.config.topic.name,
                               num, filedata)
        self.socialPlugin.logout()

    def add_future_posts(self, frompath):
        self.storageAdmin.store_all(self.config.topic.name, frompath)

    def download_future_posts(self):
        self.storageAdmin.store_all(self.config.topic.name, None)

    def register_app(self):
        self.socialPlugin.register()

    def resolve_storage_admin(self):
        storageModuleObj = Brains._module(K.packageName, K.storageModule,
                                          self.config.dev.storagemodule)
        storageClassObj = getattr(
            storageModuleObj, self.config.dev.storageclass)
        return storageClassObj

    def resolve_social_plugin(self):
        socialModuleObj = Brains._module(K.packageName, K.socialModule,
                                         self.config.dev.socialmodule)
        socialPluginClassObj = getattr(
            socialModuleObj, self.config.dev.socialclass)
        return socialPluginClassObj

    @staticmethod
    def process_args():
        """
        handles command line options and flags
        """
        example_usage_text = '''Example:

        ./bot.py  -c ./config.yaml

        '''
        parser = argparse.ArgumentParser(
            description="Wakes up infobot to post",
            epilog=example_usage_text,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--confpath",
                            help="path for yaml configuration file",
                            type=str, default="./config.yaml")
        parser.add_argument("-a", "--addfrompath",
                            help="move entries from a directory" +
                                 " to bot storage",
                            type=str, required=False)
        parser.add_argument("-d", "--download",
                            help="downloads data from a URL specified " +
                                 " in config file",
                            action="store_true",
                            default=False, required=False)
        parser.add_argument("-r", "--registerapp",
                            help="one time app registration is required" +
                            " for some social plugins",
                            action="store_true",
                            default=False, required=False)
        parser.add_argument("-l", "--liststatus",
                            help="list current settings and status " +
                            "for some social plugins",
                            action="store_true",
                            default=False, required=False)
        args = parser.parse_args()
        return args

    @staticmethod
    def _get_config_file_name(args):
        return Brains.expand_home(args.confpath)

    @staticmethod
    def _module(packagename, dirname, modulename):
        return importlib.import_module(
            packagename + "." +
            dirname + modulename, package=packagename)

    @staticmethod
    def expand_home(origPath):
        if "~" in origPath:
            origPath = origPath.replace("~",
                                        str(os.path.expanduser('~')))
        return origPath
