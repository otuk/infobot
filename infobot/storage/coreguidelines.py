import os
import yaml
import pickle
import requests
from lxml import html

import infobot.konstants as K
from infobot.storage.template import Admin
from infobot.config import Admin as ConfigAdm
from infobot.brains import Brains


class CoreListConf():
    def __init__(self, corelistdetails):
        "Configurations Object for Core Guidelines Pickled List Object"
        self.directory = Brains.expand_home(
            corelistdetails[K.dataDirectoryKey])
        self.counterfile = Brains.expand_home(
            corelistdetails[K.counterKey])
        self.picklefile = Brains.expand_home(
            corelistdetails[K.pickleFileKey])
        self.downloadurl = corelistdetails[K.downloadUrlKey]


class CoreList(Admin):
    def __init__(self, config, corelistdetails):
        """
        This is a file system based storage admin.
        It stores each information to be posted as a separate file
        It also keeps track of the number of items to be posted
        """
        super().__init__(config)
        self._details = CoreListConf(corelistdetails)
        self._directory = self._details.directory
        self._counterfile = self._details.counterfile
        self._picklefile = self._details.picklefile
        self._downloadurl = self._details.downloadurl
        self._datalist = []
        self.get_list_data()

    def status(self):
        print("CoreList Storage Admin is active")
        print("  Using data downloaded from: {}".format(
            self._downloadurl
        ))
        print("  Reading posts from binary file: {}".format(
            self._picklefile
        ))
        print("  Counter file at: {}".format(
            self._counterfile
        ))
        start, last, previous = self.get_counters()
        print("  There are {} posts, last post index is: {}".format(
            str(len(self._datalist)),
            str(last)
        ))

    def format_index(self, topic, num):
        """
        returns formatted  filename
        """
        return num

    def read_from(self, index):
        """
        Returns the postable data at the index location
        """
        if self._datalist is not None:
            if len(self._datalist) > 0:
                num, rule, url = self._datalist[index]
        return num + "\n" + rule + "\n" + url

    def get_counters(self):
        counterData = ConfigAdm.read_yaml(self._counterfile)
        return (int(counterData[K.startKey]),
                int(counterData[K.lastKey]),
                int(counterData[K.previousKey]))

    def increment_last(self):
        with open(self._counterfile, "r") as f:
            data = yaml.safe_load(f)
            data[K.lastKey] = len(self._datalist) - 1
        with open(self._counterfile, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    def store_all(self, topic, url):
        if url is None:
            url = self._downloadurl
        print(("Will download the data for {}\n"
               "from the website: {}\n"
               "into: {}")
              .format(self.config.topic.name,
                      url,
                      self._directory))
        self.get_list_data()

    def get_list_data(self):
        data_list_file = self._picklefile
        if not os.path.exists(data_list_file):
            # if data_list does not exists download
            self._datalist = self.download_data(self._downloadurl)
            # store the data_list
            with open(data_list_file, "wb") as f:
                pickle.dump(self._datalist, f)
            self.increment_last()
        else:
            print("Pickle file in place no need to download")
            # load the data_list
            with open(data_list_file, "rb") as f:
                self._datalist = pickle.load(f)

    @staticmethod
    def download_data(url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        titles = tree.xpath('//div/h3[@id]')
        anchors = tree.xpath('//div/h3[@id]/a[1]')
        data_list = []
        for i, (t, a) in enumerate(zip(titles[:454], anchors[:454])):
            text = ""
            cs = t.getchildren()
            ts = t.xpath('./text()')
            lcs = len(cs)
            lts = len(ts)
            # print("@",lcs)
            # print("@",lts)
            if lts == lcs and lts == 1:
                text = ts[0]
                #  print(i, ":", ts[0])
            elif lts == lcs and lts > 1:
                text = ts[0]
                for s1, s2 in zip(ts[1:], cs[1:]):
                    text += (s2.text_content() + " " + s1 + " ")
            elif lts < lcs:
                text = ts[0]
                for s1, s2 in zip(ts[1:], cs[1:-1]):
                    text += (s2.text_content() + " " + s1 + " ")
                text += cs[-1].text_content()
            no, rule = text.split(":", 1)
            data_list.append((no, rule.strip(), url + "#" + t.attrib['id']))
        return data_list

    def store(self, topic, data):
        pass

    def get_header(self, socialNetwork, topic, _):
        header = CoreList.templates[socialNetwork][K.headerKey]
        return header.format(topic)

    def get_footer(self, socialNetwork, topic, _):
        footer = CoreList.templates[socialNetwork][K.footerKey]
        return footer.format(topic)

    templates = {
        K.fakeKey:
        {
            K.headerKey: """#{}""",

            K.footerKey: """
------
Please reply to report error"""
        },
        K.mastodonKey:
        {
            K.headerKey:  "#{}",

            K.footerKey: ""
        }

    }
