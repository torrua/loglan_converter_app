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

db = SQLAlchemy()


class CLIConfig:
    """
    Configuration object for remote database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from config.postgres import model_base

all_models_pg = sorted(
    [model for model in model_base.DictionaryBase.__subclasses__()],
    key=lambda model: model.__index_sort_import__)

models_pg_from_file = [model for model in all_models_pg if model.__load_from_file__]
models_pg_to_db = [model for model in all_models_pg if model.__load_to_db__]
models_pg_for_stat = tuple(models_pg_to_db)

EXPORT_PG_DIRECTORY_PATH_LOCAL = os.getenv("EXPORT_DIRECTORY_PATH_LOCAL", f"{root_directory}export\\")


def db_get_statistic(db_models: tuple = models_pg_for_stat):
    """
    :param db_models:
    :return:
    """
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info("%s: %s", model.__name__, model.query.count())
    log.info("Finish to get statistic of imported items\n")


def db_get_property():
    """
    :return:
    """
    objects = model_base.Word.query.all()
    objects_str = [obj.rank for obj in objects]
    print(len(objects_str))
    maxi = max(objects_str, key=len)
    print(maxi, len(maxi))


def check_db_connection(db_uri):
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


def run_with_context(function):

    def wrapper(*args, **kwargs):

        db_uri = os.environ.get('LOD_DATABASE_URL', None)
        if not db_uri:
            log.error("Please, specify 'LOD_DATABASE_URL' variable.")
            return

        class AppConfig:
            SQLALCHEMY_DATABASE_URI = db_uri
            SQLALCHEMY_TRACK_MODIFICATIONS = False

        try:
            context = create_app(AppConfig).app_context()
        except ValueError as err:
            log.error(err)
            return

        context.push()
        function(*args, **kwargs)
        context.pop()

    return wrapper
