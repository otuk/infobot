import os
import yaml

import infobot.konstants as K
from infobot.storage.template import Admin
from infobot.config import Admin as ConfigAdm
from infobot.brains import Brains


class FileAdminConf():
    def __init__(self, fileadmindetails):
        "Configurations Object for File based storage admin"
        self.directory = Brains.expand_home(
            fileadmindetails[K.dataDirectoryKey])
        self.counterfile = Brains.expand_home(
            fileadmindetails[K.counterKey])
        self.indexFileFormat = fileadmindetails[K.indexFileFormatKey]


class FileAdmin(Admin):
    def __init__(self, config, fileadmindetails):
        """
        This is a file system based storage admin.
        It stores each information to be posted as a separate file
        It also keeps track of the number of items to be posted
        """
        super().__init__(config)
        self._details = FileAdminConf(fileadmindetails)
        self._directory = self._details.directory
        self._counterfile = self._details.counterfile
        self._indexFileFormat = self._details.indexFileFormat

    def status(self):
        print("File Based Storage Admin is active")
        print("  Reading posts from: {}".format(
            self._directory
        ))
        print("  Counter file at: {}".format(
            self._counterfile
        ))
        start, last, previous = self.get_counters()
        print("  There are {} posts, last post index is: {}".format(
            str(last - start + 1),
            str(last)
        ))

    def format_index(self, topic, num):
        """
        returns formatted  filename
        """
        return self._indexFileFormat.format(topic, str(num))

    def read_from(self, index):
        """
        Returns the postable data at the index location
        """
        fullpath = os.path.join(self._directory, index)
        with open(fullpath) as postfile:
            postdata = postfile.read()
        return postdata

    def get_counters(self):
        counterData = ConfigAdm.read_yaml(self._counterfile)
        return (int(counterData[K.startKey]),
                int(counterData[K.lastKey]),
                int(counterData[K.previousKey]))

    def increment_last(self):
        with open(self._counterfile, "r") as f:
            data = yaml.safe_load(f)
            cl = int(data[K.lastKey])
            data[K.lastKey] = cl + 1
        with open(self._counterfile, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    def store_all(self, topic, fromdir):
        print(("Will move files with name containing {}\n"
               "from: {}\n"
               "into: {}")
              .format(self.config.topic.name,
                      fromdir,
                      self._directory))
        fromdir = Brains.expand_home(fromdir)
        for f in os.listdir(fromdir):
            sourceFile = os.path.join(fromdir, f)
            print(sourceFile)
            if os.path.isdir(f) or (topic not in str(f)):
                continue
            with open(sourceFile) as fd:
                data = fd.read()
                self.store(topic, data)
                os.remove(sourceFile)

    def store(self, topic, data):
        _, last, _ = self.get_counters()
        num = last+1
        filename = self.format_index(topic, num)
        fullpath = os.path.join(self._directory, filename)
        with open(fullpath, "w") as f:
            f.write(data)
            self.increment_last()

    def get_header(self, socialNetwork, topic, num):
        header = FileAdmin.templates[socialNetwork][K.headerKey]
        return header.format(topic, num)

    def get_footer(self, socialNetwork, topic, num):
        footer = FileAdmin.templates[socialNetwork][K.footerKey]
        return footer.format(topic, num)

    templates = {
        K.fakeKey:
        {
            K.headerKey: """
            #{}-{}""",

            K.footerKey: """
------
Please reply to report error"""

        },
        K.mastodonKey:
        {
            K.headerKey:  "#{}-{}\n",

            K.footerKey: ""
        }

    }
