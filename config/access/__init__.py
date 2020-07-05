# -*- coding: utf-8 -*-
""""
Module for configuration data of AC database
"""
import urllib
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import log, root_directory

__all__ = ["ac_create_engine", "Base", "db_get_statistic", "EXPORT_AC_DIRECTORY_PATH_LOCAL",
           "MDB_FILE_PATH", "ac_session", "models_ac", "EXPORT_AC_FILE_PATHS_LOCAL"]

MDB_FILE_PATH = os.getenv("MDB_FILE_PATH", f"{root_directory}LoglanDictionary.mdb")


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

models_ac = Base.__subclasses__()

# IMPORT_AC_DIRECTORY_PATH_LOCAL = os.getenv('IMPORT_DIRECTORY_PATH_LOCAL', f"{root_directory}import\\")
# IMPORT_AC_FILE_PATHS_LOCAL = [IMPORT_AC_DIRECTORY_PATH_LOCAL + model.import_file_name for model in models_ac]

EXPORT_AC_DIRECTORY_PATH_LOCAL = os.getenv("EXPORT_DIRECTORY_PATH_LOCAL", f"{root_directory}export\\")
EXPORT_AC_FILE_PATHS_LOCAL = [EXPORT_AC_DIRECTORY_PATH_LOCAL + model.export_file_name for model in models_ac]


def db_get_statistic(db_models: list = models_ac):
    """

    :param db_models:
    :return:
    """
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info(f"%s: %s", model.sort_name, ac_session.query(model).count(), )
    log.info("Finish to get statistic of imported items\n")


def db_get_property():
    objects = ac_session.query(model_dictionary.AccessWord).all()
    objects_str = [obj.rank for obj in objects if obj.rank]
    print(len(objects_str))
    maxi = max(objects_str, key=len)
    print(maxi, len(maxi))


if __name__ == "__main__":
    db_get_property()
