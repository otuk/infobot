#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `infobot` package.
Module tested:  config
"""

import pytest

from infobot.config import Admin as ConfigAdmin

# from click.testing import CliRunner
# from infobot import cli


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


def test_config():
    config = ConfigAdmin("./config.yaml")
    assert(config.topic.name == "rust")
    assert(config.dev.storageclass == "FileAdmin")
    assert(config.randomizer.ontimes == 24)
    assert(config.randomizer.outoftimes == 24)
    # assert(config.topic.opt == "")  # optional field
