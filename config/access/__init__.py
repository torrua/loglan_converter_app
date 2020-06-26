# -*- coding: utf-8 -*-
""""
Module for configuration data of AC database
"""

import urllib
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import log

__all__ = ["ac_create_engine", "Base", "db_get_statistic", "MDB_FILE_PATH", "ac_session", ]

MDB_FILE_PATH = os.getenv("MDB_FILE_PATH")


def ac_create_engine(db_path):
    """
    :param db_path:
    :return:
    """
    connection_string = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        fr'DBQ={db_path};'
        r'ExtendedAnsiSQL=1;')
    connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
    return create_engine(connection_url)


engine = ac_create_engine(MDB_FILE_PATH)

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)
ac_session = session()


def ac_create_all():
    """
    :return:
    """
    Base.metadata.create_all(engine)


from config.access import model_dictionary


def db_get_statistic(db_models: list = model_dictionary.models_ac):
    """

    :param db_models:
    :return:
    """
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info(f"%s: %s", model.sort_name, ac_session.query(model).count(), )
    log.info("Finish to get statistic of imported items\n")
