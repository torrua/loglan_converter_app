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

from config import log


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


def db_get_statistic(db_models: list = model_dictionary.models_pg):
    """

    :param db_models:
    :return:
    """
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info("%s: %s", model.__name__, model.query.count())
    log.info("Finish to get statistic of imported items\n")


if __name__ == "__main__":
    db_get_statistic()
