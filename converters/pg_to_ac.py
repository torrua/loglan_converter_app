# -*- coding: utf-8 -*-
""""Module for uploading data from PG database to AC database"""
import time
from datetime import timedelta

from config import log, SEPARATOR
from config.access import MDB_FILE_PATH as AC_PATH, db_get_statistic, session

from config.postgres.model_export import export_models_pg
from converters.pg_to_txt import export_pg_model_to_list_of_str
from converters.txt_to_ac import db_backup_file, db_clear_content, db_compress_file
from config.access.model_export import export_models_ac


def get_data_from_schema():
    """

    :return:
    """
    log.info("Starting to export data from db")
    convert_schema = zip(export_models_pg, export_models_ac)
    # TODO Add logging
    ac_session = session()
    for export_model, import_model in convert_schema:
        log.info("Starting %s export", export_model.__name__)
        raw_table_lines = export_pg_model_to_list_of_str(export_model)
        prepared_lines = [line.strip().split(SEPARATOR) for line in raw_table_lines]
        objects = [import_model(**import_model.import_(line)) for line in prepared_lines]
        ac_session.bulk_save_objects(objects)
        ac_session.commit()
        log.info("Ending %s export - %s object(s)", export_model.__name__, len(objects))
    ac_session.close()
    log.info("Ending db export\n")


def convert_pg_to_ac(db_path: str = AC_PATH) -> None:
    """
    Complete new db generation. It remove previous db with all data
    and fill the new one with data from txt files

    The data from the source text files is added in two stages -
    first the data itself, and then the relationship between it

    :return: None
    """

    log.info("START DB CREATION")
    start_time = time.monotonic()

    log.info("MILESTONE: Create backup for DB")
    db_backup_file(db_path=db_path)

    log.info("MILESTONE: Clear all existing tables in DB")
    db_clear_content(db_path=db_path)

    log.info("MILESTONE: Fill tables in new DB")
    get_data_from_schema()

    log.info("MILESTONE: Delete backup")
    db_backup_file(db_path=db_path, remove=True)

    log.info("MILESTONE: Compress DB")
    db_compress_file(db_path=db_path)

    log.info("ELAPSED TIME IN MINUTES: %s\n",
             timedelta(minutes=time.monotonic() - start_time))

    db_get_statistic()
    log.info("FINISH DB CREATION")


if __name__ == "__main__":
    convert_pg_to_ac()
