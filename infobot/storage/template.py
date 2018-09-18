
class Admin():
    def __init__(self, config):
        "abstract"
        self.config = config
        pass

    def store(self, data, toIndex):
        raise NotImplementedError()

    def read_from(self, index):
        raise NotImplementedError()

    def get_indices(self):
        raise NotImplementedError()

    def format_index(self, topicname, num):
        raise NotImplementedError()

    def get_header(self, socialnetwork, topic, num):
        raise NotImplementedError()

    def get_footer(self, socialnetwork, topic, num):
        raise NotImplementedError()
