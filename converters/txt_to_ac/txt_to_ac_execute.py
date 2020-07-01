# -*- coding: utf-8 -*-
"""Module for generating LOD dictionary database from txt files"""
import os
import shutil
import time
from datetime import timedelta

import win32com.client
from sqlalchemy import MetaData

from config import log
from config.access import ac_create_engine, MDB_FILE_PATH as AC_PATH, db_get_statistic
from config.text import IMPORT_DIRECTORY_PATH_LOCAL
from converters.txt_to_ac.txt_to_ac_functions_fill import db_fill_tables


def db_backup_file(db_path, suffix: str = "backup", remove: bool = False):
    """
    :param db_path:
    :param suffix:
    :param remove:
    :return:
    """
    if not remove:
        shutil.copy(db_path, db_path.replace(".mdb", f"_{suffix}.mdb"))
    else:
        os.remove(db_path.replace(".mdb", f"_{suffix}.mdb"))


def db_clear_content(db_path):
    """
    :param db_path:
    :return:
    """
    engine = ac_create_engine(db_path)
    meta = MetaData()
    meta.reflect(bind=engine)

    for table in reversed(meta.sorted_tables):
        engine.execute(table.delete())
    engine.dispose()


def db_compress_file(db_path):
    """
    :param db_path:
    :return:
    """

    dst_db = db_path.replace(".mdb", "_temp.mdb")
    os_app = win32com.client.Dispatch("Access.Application")
    os_app.compactRepair(db_path, dst_db)
    os_app.Application.Quit()
    os.remove(db_path)
    os.rename(dst_db, db_path)


def convert_txt_to_ac(db_path: str = AC_PATH, source_path: str = IMPORT_DIRECTORY_PATH_LOCAL) -> None:
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

    log.info("MILESTONE: Compress DB")
    db_compress_file(db_path=db_path)

    log.info("MILESTONE: Fill tables in new DB")
    db_fill_tables(source_path=source_path)

    log.info("MILESTONE: Delete backup")
    db_backup_file(db_path=db_path, remove=True)

    log.info("ELAPSED TIME IN MINUTES: %s\n",
             timedelta(minutes=time.monotonic() - start_time))

    db_get_statistic()
    log.info("FINISH DB CREATION")


if __name__ == "__main__":
    convert_txt_to_ac()
