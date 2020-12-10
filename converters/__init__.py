# -*- coding: utf-8 -*-
"""
Module for common converters settings and functions
"""

import os
from config import log, root_directory, DEFAULT_LANGUAGE


def db_get_statistic(models_list):
    """
    :return:
    """
    log.info("Start to get statistic of imported items:")
    [log.info("%s: %s", model.__name__, model.query.count())
     for model in models_list if model.__load_to_db__]
    log.info("Finish to get statistic of imported items\n")


def db_get_property_info(cls, prop: str):
    """
    :param cls:
    :param prop:
    :return:
    """
    objects_str = [getattr(obj, prop) for obj in cls.query.all()]
    print("NUMBER OF OBJECTS: %s" % len(objects_str))
    maxi = max(objects_str, key=len)
    print("MAX LENGTH: %s (for '%s')" % (len(maxi), maxi))
    mini = min(objects_str, key=len)
    print("MIN LENGTH: %s (for '%s')" % (len(mini), mini))
