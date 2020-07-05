# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0413

"""
Initializing application module
Create an application object and database
"""

import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import log, root_directory


class Config:
    """
    Configuration object for remote database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from config.postgres import model_dictionary

all_models_pg = sorted(
    [model for model in model_dictionary.BaseFunctions.__subclasses__()],
    key=lambda model: model.__index_sort_import__)

models_pg_from_file = [model for model in all_models_pg if model.__load_from_file__]
models_pg_to_db = [model for model in all_models_pg if model.__load_to_db__]
models_pg__for_stat = tuple(models_pg_to_db)

EXPORT_PG_DIRECTORY_PATH_LOCAL = os.getenv("EXPORT_DIRECTORY_PATH_LOCAL", f"{root_directory}export\\")
EXPORT_PG_FILE_PATHS_LOCAL = [EXPORT_PG_DIRECTORY_PATH_LOCAL + model.export_file_name for model in models_pg_from_file]


def db_get_statistic(db_models: tuple = models_pg__for_stat):
    """
    :param db_models:
    :return:
    """
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info("%s: %s", model.__name__, model.query.count())
    log.info("Finish to get statistic of imported items\n")


def db_get_property():
    objects = model_dictionary.Word.query.all()
    objects_str = [obj.rank for obj in objects]
    print(len(objects_str))
    maxi = max(objects_str, key=len)
    print(maxi, len(maxi))


if __name__ == "__main__":
    db_get_property()
