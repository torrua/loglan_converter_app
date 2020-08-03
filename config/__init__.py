# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Configuration file for the whole project
"""
import sys
import re
import logging
from flask import Flask


logging.basicConfig(
    format='%(message)s',
    # format='%(filename)s [LINE:%(lineno)d]\t[%(asctime)s] %(levelname)-s\t%(funcName)s() \t\t%(message)s',
    level=logging.DEBUG,
    datefmt="%y-%m-%d %H:%M:%S")

log = logging.getLogger(__name__)

EN = "en"
DEFAULT_LANGUAGE = EN
SEPARATOR = "@"

root_pattern = r".*\\"
root_directory = re.search(root_pattern, sys.executable)[0]


def create_app(config):
    """
    Create app
    """

    # app initialization
    app = Flask(__name__)

    app.config.from_object(config)

    # db initialization
    from config.postgres.model_base import db

    db.init_app(app)
    # db.create_all(app=app) when use need to re-initialize db

    return app
