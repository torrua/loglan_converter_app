# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""
Common functions for text files
"""

import time
from datetime import timedelta
from os import path, makedirs

from config import log
from config.text import EXPORT_DIRECTORY_PATH


def save_to_file(elements, file_path) -> None:
    """Save list of str to text file"""
    with open(file_path, "w+", encoding="utf-8") as file:
        file.write("\n".join(elements))
    file.close()

    log.info("%s items exported to %s", len(elements), file_path.replace(r"\\", '\\'))


def convert_schema_to_txt(export_schema: dict, converter, file_suffix: str):
    """

    :return:
    """
    log.info("Starting db export")
    start_time = time.monotonic()

    if not path.isdir(EXPORT_DIRECTORY_PATH):
        log.debug("Creating export directory: %s", EXPORT_DIRECTORY_PATH)
        makedirs(EXPORT_DIRECTORY_PATH)
    for export_path, export_model in export_schema.items():
        log.info("Starting %s export", export_model.__name__)
        elements = converter(export_model)
        save_to_file(elements, export_path.replace(".txt", f"_{file_suffix}.txt"))
        log.info("Ending %s export\n", export_model.__name__)

    log.info("ELAPSED TIME IN MINUTES: %s\n", timedelta(minutes=time.monotonic() - start_time))
    log.info("Ending db export\n")
