# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Configuration file for the whole project
"""

import logging

logging.basicConfig(
    format='%(filename)s [LINE:%(lineno)d]\t[%(asctime)s] '
           '%(levelname)-s\t%(funcName)s() \t\t%(message)s',
    level=logging.INFO,
    datefmt="%y-%m-%d %H:%M:%S")
log = logging.getLogger(__name__)
