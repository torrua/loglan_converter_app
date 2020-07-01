# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""
Common functions for text files
"""

import time
from datetime import timedelta
from os import path, makedirs
from typing import List

import requests

from config import log, SEPARATOR
from config.access import EXPORT_AC_DIRECTORY_PATH_LOCAL


def save_to_file(elements, file_path) -> None:
    """Save list of str to text file"""
    with open(file_path, "w+", encoding="utf-8") as file:
        file.write("\n".join(elements))
    file.close()

    log.info("%s items exported to %s", len(elements), file_path.replace(r"\\", '\\'))


def convert_schema_to_txt(
        export_schema: dict, converter, file_suffix: str = "",
        export_directory_path: str = EXPORT_AC_DIRECTORY_PATH_LOCAL):
    """

    :return:
    """
    log.info("Starting db export")
    start_time = time.monotonic()

    if not path.isdir(export_directory_path):
        log.debug("Creating export directory: %s", export_directory_path)
        makedirs(export_directory_path)
    for export_path, export_model in export_schema.items():
        log.info("Starting %s export", export_model.__name__)
        elements = converter(export_model)
        save_to_file(elements, export_path.replace(".txt", f"_{file_suffix}.txt"))
        log.info("Ending %s export\n", export_model.__name__)

    log.info("ELAPSED TIME IN MINUTES: %s\n", timedelta(minutes=time.monotonic() - start_time))
    log.info("Ending db export\n")


def download_dictionary_file(url: str, model_name: str,
                             separator: str = SEPARATOR) -> List[List[str]]:
    """
    Convert text file downloaded from the Github to the python list
        where each item is a list with line's elements
    :param url:
    :param model_name:
    :param separator: separation symbol, '@' by default
    :return: prepared python list
    """

    log.debug("Start to get '%s' content", model_name)

    if str(url).startswith("http"):
        lines = requests.get(url).text.split("\n")
    else:
        file = open(url, 'r', encoding="utf-8")
        lines = file.read().split("\n")

    log.debug("Finish to get '%s' content\n", model_name)
    return [file_line.strip().split(separator) for file_line in lines if file_line]
