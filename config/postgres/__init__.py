# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0413

"""
Initializing application module
Create an application object and database
"""

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from config import log, DEFAULT_LANGUAGE, root_directory, create_app

LOD_KEY_DEFAULT_LANGUAGE = os.getenv("LOD_KEY_DEFAULT_LANGUAGE", DEFAULT_LANGUAGE)
EXPORT_PG_DIRECTORY_PATH_LOCAL = os.getenv("EXPORT_DIRECTORY_PATH_LOCAL", f"{root_directory}export\\")
LOD_DATABASE_URL = os.environ.get('LOD_DATABASE_URL', None)

db = SQLAlchemy()

from config.postgres import model_base


class CLIConfig:
    """
    Configuration object for remote database
    """
    SQLALCHEMY_DATABASE_URI = LOD_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


all_models_pg = sorted(
    [model for model in model_base.DictionaryBase.__subclasses__()],
    key=lambda model: model.__index_sort_import__)


def db_get_statistic(models: all_models_pg):
    """
    :return:
    """
    log.info("Start to get statistic of imported items:")
    [log.info("%s: %s", model.__name__, model.query.count())
     for model in models if model.__load_to_db__]
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


def is_db_connected(db_uri: str) -> bool:
    """
    :param db_uri:
    :return:
    """
    try:
        eng = create_engine(db_uri)
        eng.execute("SELECT 1")
    except:
        return False
    else:
        eng.dispose()
        return True


def app_lod(config_lod):
    """
    Create app
    """
    return create_app(config_lod, database=db)


def run_with_context(function):

    def wrapper(*args, **kwargs):

        db_uri = os.environ.get('LOD_DATABASE_URL', None)

        if not db_uri:
            log.error("Please, specify 'LOD_DATABASE_URL' variable.")
            return

        class AppConfig:
            SQLALCHEMY_DATABASE_URI = LOD_DATABASE_URL
            SQLALCHEMY_TRACK_MODIFICATIONS = False

        try:
            context = app_lod(AppConfig).app_context()
        except ValueError as err:
            log.error(err)
            return

        context.push()
        function(*args, **kwargs)
        context.pop()

    return wrapper


if __name__ == "__main__":

    with app_lod(CLIConfig).app_context():
        pass
