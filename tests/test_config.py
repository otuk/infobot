#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `infobot` package."""

import pytest

from click.testing import CliRunner

from infobot import cli


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


def test_config():
    data = ConfigAdmin.read_yaml("./config.yaml")
    config = ConfigAdmin(data)
    assert(config.topic.name == "rust")
    assert(config.topic.storageclass == "FileAdmin")
    assert(config.topic.opt == "")  # optional field
    assert(config.randomizer.ontimes == 24)
    assert(config.randomizer.outoftimes == 24)
