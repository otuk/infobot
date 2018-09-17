#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `infobot` package."""

import pytest


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


from infobot.config import Admin as ConfigAdmin    
from infobot.storage import FileAdmin as FileAdmin


def test_config():
    data = ConfigAdmin.read_yaml("./config.yaml")
    config = ConfigAdmin(data)
    fa = FileAdmin(config, config.storageadmindetails)
    assert(fa._directory == "~/Nextcloud/Documents/rusty_robot/")
    assert(fa._indexfile == "~/Nextcloud/Documents/rusty_robot/last.txt")
