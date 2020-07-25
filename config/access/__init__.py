# -*- coding: utf-8 -*-
# pylint: disable=E1101

""""
Module for configuration data of AC database
"""

import os
import urllib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import log, root_directory

__all__ = ["ac_create_engine", "Base", "db_get_statistic",
           "EXPORT_AC_DIRECTORY_PATH_LOCAL", "engine",
           "MDB_FILE_PATH", "session", "models_ac", ]

MDB_FILE_PATH = os.getenv(
    "MDB_FILE_PATH",
    f"{root_directory}LoglanDictionary.mdb")


def ac_create_engine(db_path):
    """
    :param db_path:
    :return:
    """
    connection_string = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        fr'DBQ={db_path};'
        r'ExtendedAnsiSQL=1;')
    connection_url = f"access+pyodbc:///?odbc_connect=" \
                     f"{urllib.parse.quote_plus(connection_string)}"
    return create_engine(connection_url)


engine = ac_create_engine(MDB_FILE_PATH)

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)


def ac_create_all():
    """
    :return:
    """
    Base.metadata.create_all(engine)


from config.access import model_dictionary

models_ac = Base.__subclasses__()
models_ac_for_stat = tuple(models_ac)

EXPORT_AC_DIRECTORY_PATH_LOCAL = os.getenv(
    "EXPORT_DIRECTORY_PATH_LOCAL",
    f"{root_directory}export\\")


def db_get_statistic(db_models: tuple = models_ac_for_stat):
    """

    :param db_models:
    :return:
    """
    ac_session = session()
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info(
            "%s: %s", model.sort_name,
            ac_session.query(model).count(), )
    ac_session.close()
    log.info("Finish to get statistic of imported items\n")
    engine.dispose()


def db_get_property():
    """
    :return:
    """
    ac_session = session()
    objects = ac_session.query(model_dictionary.AccessWord).all()
    objects_str = [obj.rank for obj in objects if obj.rank]
    print(len(objects_str))
    maxi = max(objects_str, key=len)
    print(maxi, len(maxi))
    ac_session.close()


if __name__ == "__main__":
    db_get_property()
