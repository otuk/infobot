import argparse
import importlib


# import infobot.konstants
from infobot.config import Admin
from infobot.index import RandomHelper


class Brains():
    """
    Brains does the main coordination for infobot.
    It works with social plugin and the storage admin
    to make the posts or add more data for future posts
    from a user supplied directory.
    """

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
    def get_config_file_name(args):
        return args.confpath

    def __init__(self):
        """
        create a coordinator for infobot
        and start him on its tasks based on
        user supplied command line arguments
        """
        args = Brains.process_args()
        configFileName = Brains.get_config_file_name(args)
        configData = Admin.read_yaml(configFileName)
        self.config = Admin(configData)
        StorageAdmin = self.resolveStorageAdmin()
        self.storageAdmin = StorageAdmin(
            self.config, self.config.storageadmindetails)
        self.randomHelper = RandomHelper(self.config, self.storageAdmin)
        self.awake(args)

    def resolveStorageAdmin(self):
        storageModuleObj = importlib.import_module(
            "infobot.storage", package="infobot")
        storageClassObj = getattr(
            storageModuleObj, self.config.topic.storageclass)
        return storageClassObj

    def awake(self, args):
        if args.addfrompath is not None:
            self.add_future_posts()
        else:
            if self.randomHelper.should_i_run():
                self.post_to_social()

    def post_to_social(self):
        num = self.randomHelper.get_random_number()
        filename = self.config.topic.name + "_" + str(num)
        filedata = self.storageAdmin.read(filename)

    # ask social to login
    # ask social to do prepost procedures
    # pass it to social to post
    # ask social to logout
    # shutdown again
        print(" oh yes posting")

    def add_future_posts(self):
        pass
        print("yes sure adding files")
