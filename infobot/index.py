import random


class RandomHelper():
    def __init__(self, config, storageAdmin):
        self.config = config
        self.storageAdmin = storageAdmin
        self.excludeList = config.randomizer.exclude
        random.seed()

    def get_counters(self):
        return self.storageAdmin.get_counters()

    def get_random_number(self):
        """
        Returns a random number to pick from
        among the available indexed posts.

        It excludes the post indexes that are in
        the exclude list in the configuration file.
        """
        start, last, previous = self.get_counters()
        ret = random.randint(start, last)
        while ret in self.excludeList:
            ret = random.randint(start, last)
        return ret

    def should_i_run(self):
        ont = self.config.randomizer.ontimes
        allt = self.config.randomizer.outoftimes
        # assumes ont is always less than or equal to allt
        assert(ont <= allt)
        return ont >= random.randint(1, allt)
