
import konstants

class Admin():

    def __init__(self, configMgr):
        "abstract"
        self.configMgr = configMgr
        pass

    def store(self, data):
        raise NotImplementedError()

    def read(self, data):
        raise NotImplementedError()

    
class FileAdmin(Admin):

    def __init__(self, configMgr):
        "docstring"
        super().__init__(configMgr)
        

    def read(self, data):
        filename = self.cofigMgr.get(konstants.k_configfile)
        with open(filename) as conf:
            

        
