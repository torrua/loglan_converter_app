# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0413

"""
Initializing translation module
Create an application object and database
"""

import os
from flask_sqlalchemy import SQLAlchemy
from config import log, create_app

db = SQLAlchemy()

from config.sqlite import model


def run_with_context(function):

    def wrapper(*args, **kwargs):

        db_uri = os.environ.get('TRANS_DATABASE_URL', None)
        if not db_uri:
            log.error("Please, specify 'TRANS_DATABASE_URL' variable.")
            return

        class AppConfig:
            SQLALCHEMY_DATABASE_URI = db_uri
            SQLALCHEMY_TRACK_MODIFICATIONS = False

        try:
            context = create_app(AppConfig, db).app_context()
        except ValueError as err:
            log.error(err)
            return

        context.push()
        function(*args, **kwargs)
        context.pop()

    return wrapper
