#!/usr/bin/env python3
from infobot.brains import Brains

    # this has 2 modes of operation
    # In one case it is intended to be woken up by a cron job
    # every hour
    #
    # in the other it imports future post entries from a directory
if __name__ == "__main__":
    # awake
    brains = Brains()
