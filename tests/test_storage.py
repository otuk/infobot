#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `infobot` package.
Module tested:  storage
"""

import pytest

from infobot.config import Admin as ConfigAdmin
from infobot.storage.file import FileAdmin as FileAdmin
from infobot.brains import Brains


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_storage():
    config = ConfigAdmin("./config.yaml")
    fa = FileAdmin(config, config.storageadmindetails)
    assert(fa._directory == Brains.expand_home(
        "~/Nextcloud/Documents/rusty_robot/data/"))
    assert(fa._counterfile == Brains.expand_home(
           "~/Nextcloud/Documents/rusty_robot/data/counter.yaml"))
