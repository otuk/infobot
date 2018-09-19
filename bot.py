#!/usr/bin/env python3
from infobot.brains import Brains
"""
This is a sample implementation of how you can
use the infobot module to store information/data
and later make posts to social networks using that data.

This executable has 2 modes of operations.
1. In one case it is intended to be woken up by a cron job (maybe every hour)
It has configuration parameters to control how often it actually posts even
if you wake it up every minute.  See config.yaml.

2. Second mode is the other when it imports future post entries
from a user supplied directory

In a typical implementaion you would be using crontab (or similar)
with and entry such as this:

# this command will run every hour 3 minutes past the hour
3 * * * * /path/to/virtual_env_for_prj/bin/python3 /full/path/bot.y  -c /full/path/config.yaml

"""


if __name__ == "__main__":
    # awake
    brains = Brains()
