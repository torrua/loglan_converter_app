# -*- coding: utf-8 -*-
"""Module for generating LOD dictionary database from txt files"""
import time
from datetime import timedelta

from config import log, DEFAULT_LANGUAGE
from config.postgres import db
from config.postgres.models import all_models_pg
from converters import db_get_statistic
from config.text import IMPORT_DIRECTORY_PATH_LOCAL
from converters.txt_to_pg.txt_to_pg_functions_fill import db_fill_tables, get_dataset_for_converters
from converters.txt_to_pg.txt_to_pg_functions_link import db_link_tables


def generic_convert_to_pg(dataset: dict):
    """
    Complete new db generation. It remove previous db with all data
    and fill the new one with data from txt files

    The data from the source text files is added in two stages -
    first the data itself, and then the relationship between it

    :return: None
    """

    log.info("START DB CREATION")
    start_time = time.monotonic()

    log.info("MILESTONE: Drop all existing tables in DB")
    db.drop_all()

    log.info("MILESTONE: Create all new tables in DB")
    db.create_all()

    log.info("MILESTONE: Fill tables in new DB")

    db_fill_tables(dataset=dataset)

    log.info("MILESTONE: Link data between tables")
    db_link_tables(dataset=dataset)

    log.info("ELAPSED TIME IN MINUTES: %s\n",
             timedelta(minutes=time.monotonic() - start_time))
    db_get_statistic(all_models_pg)
    log.info("FINISH DB CREATION\n")


def convert_txt_to_pg(source_directory: str = IMPORT_DIRECTORY_PATH_LOCAL) -> None:
    dataset = get_dataset_for_converters(source_path=source_directory, language=DEFAULT_LANGUAGE)
    generic_convert_to_pg(dataset=dataset)


if __name__ == "__main__":
    convert_txt_to_pg()
