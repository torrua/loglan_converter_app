# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Configuration file for the whole project
"""
import os
import sys
import re
import logging


logging.basicConfig(
    # format='%(message)s',
    format='%(filename)s [LINE:%(lineno)d]\t[%(asctime)s] %(levelname)-s\t%(funcName)s() \t\t%(message)s',
    level=logging.INFO,
    datefmt="%y-%m-%d %H:%M:%S")

log = logging.getLogger(__name__)

EN, RU = "en", "ru"
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", EN)
SEPARATOR = "@"
root_pattern = r".*\\"

try:
    root_directory = re.search(root_pattern, sys.executable)[0]
except TypeError as err:
    log.warning("Cannot define root directory: %s", err)
    root_directory = None
