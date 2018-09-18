import argparse
import importlib
from pathlib import Path

# import infobot.konstants
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
        self.awake(args)

    def awake(self, args):
        """
        There are two modes of operations
        Main mode is to wake up and make a post to a social network
        The other one is when future posts are added to a storage destination
        """
        if args.addfrompath is not None:
            self.add_future_posts(args.addfrompath)
        else:
            if self.randomHelper.should_i_run():
                self.post_to_social()

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

    # ask social to do prepost procedures
    # pass it to social to post
    # ask social to logout
    # shutdown again

    def add_future_posts(self, frompath):
        pass
        print("yes sure adding files from ", frompath)

    def resolve_storage_admin(self):    # watchout the `.`
        storageModuleObj = Brains._module("infobot", "storage.",
                                          self.config.topic.storagemodule)
        storageClassObj = getattr(
            storageModuleObj, self.config.topic.storageclass)
        return storageClassObj

    def resolve_social_plugin(self):   # watchout the `.`
        socialModuleObj = Brains._module("infobot", "social.",
                                         self.config.topic.socialmodule)
        socialPluginClassObj = getattr(
            socialModuleObj, self.config.topic.socialclass)
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
                                        str(Path.home()))
        return origPath
