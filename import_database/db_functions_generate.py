# -*- coding: utf-8 -*-
"""Module for generating LOD dictionary database"""

from import_database import db, DEFAULT_LANGUAGE, log
from import_database.db_functions_link import db_link_tables
from import_database.db_functions_fill import db_fill_tables


def db_recreate_db() -> None:
    """
    Complete new db generation. It remove previous db with all data
    and fill the new one with data from txt files

    The data from the source text files is added in two stages -
    first the data itself, and then the relationship between it

    :return: None
    """

    log.debug("Start DB creation")
    log.debug("Drop all existing tables in DB")
    db.drop_all()

    log.debug("Create all new tables in DB")
    db.create_all()

    log.debug("Fill tables in new DB")
    db_fill_tables(DEFAULT_LANGUAGE)
    log.debug("Link data between tables")
    db_link_tables()
    log.debug("Finish DB creation")


if __name__ == "__main__":
    db_recreate_db()
