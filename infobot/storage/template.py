
class Admin():
    def __init__(self, config):
        "abstract"
        self.config = config
        pass

    def status(self):
        raise NotImplementedError()

    def store_all(self, topic, fromdir):
        raise NotImplementedError()

    def store(self, data, toIndex):
        raise NotImplementedError()

    def read_from(self, index):
        raise NotImplementedError()

    def get_counters(self):
        raise NotImplementedError()

    def increment_last(self):
        raise NotImplementedError()

    def format_index(self, topicname, num):
        raise NotImplementedError()

    def get_header(self, socialnetwork, topic, num):
        raise NotImplementedError()

    def get_footer(self, socialnetwork, topic, num):
        raise NotImplementedError()
