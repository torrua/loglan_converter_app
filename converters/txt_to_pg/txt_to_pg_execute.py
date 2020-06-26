# -*- coding: utf-8 -*-
"""Module for generating LOD dictionary database from txt files"""
import time
from datetime import timedelta

from converters.txt_to_pg.txt_to_pg_functions_link import db_link_tables, get_word_dataset
from converters.txt_to_pg.txt_to_pg_functions_fill import db_fill_tables, get_txt_dataset
from config.postgres import db, db_get_statistic
from config import log, DEFAULT_LANGUAGE


def generic_convert_to_pg(dataset: tuple, word_dataset: list):
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
    db_fill_tables(dataset)

    log.info("MILESTONE: Link data between tables")
    db_link_tables(word_dataset)

    log.info("ELAPSED TIME IN MINUTES: %s\n",
             timedelta(minutes=time.monotonic() - start_time))
    db_get_statistic()
    log.info("FINISH DB CREATION\n")


def convert_txt_to_pg() -> None:
    dataset = get_txt_dataset(DEFAULT_LANGUAGE)
    word_dataset = get_word_dataset()
    generic_convert_to_pg(dataset, word_dataset)


if __name__ == "__main__":
    convert_txt_to_pg()
