import argparse
import importlib


# import infobot.konstants
from infobot.config import Admin


def process_args():
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
                        help="move entries from a directory to bot storage",
                        type=str, required=False)
    args = parser.parse_args()
    return args


def get_config_file_name(args):
    return args.confpath


class Brains():
    """
    Brains does the main coordination for infobot.
    It works with social plugin and the storage admin
    to make the posts or add more data for future posts
    from a directory.
    """

    def __init__(self):
        args = process_args()
        configFileName = get_config_file_name(args)
        configData = Admin.read_yaml(configFileName)
        self.config = Admin(configData)
        self.storageAdmin = self.resolveStorageAdmin()(
            self.config, self.config.storageadmindetails)
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
            self.post_to_social()

    def post_to_social(self):
        self.storageAdmin.read()
    # parse the config file
    # initialize storage admin
    # initialize brains?
    # checkrandomizer
    # get random text #
    # ask for text
    # ask social to login
    # ask social to do prepost procedures
    # pass it to social to post
    # ask social to logout
    # shutdown again
        print(" oh yes posting")

    def add_future_posts(self):
        pass
        print("yes sure adding files")
