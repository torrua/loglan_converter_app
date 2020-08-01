# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""
Common functions for text files
"""

import time
from datetime import timedelta
import os
from typing import List

import requests

from config import log, SEPARATOR
from config.text import EXPORT_DIRECTORY_PATH_LOCAL, root_directory


def save_to_file(output_file_path, elements) -> None:
    """Save list of str to text file"""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w+", encoding="utf-8") as file:
        file.write("\n".join(elements))
    file.close()
    log.info("%s items exported to %s", len(elements), output_file_path.replace(r"\\", '\\'))


def convert_db_to_txt(export_models: list, exporter, output_directory: str = EXPORT_DIRECTORY_PATH_LOCAL):
    """

    :param export_models:
    :param exporter:
    :param output_directory:
    :return:
    """

    log.info("Starting db export")
    start_time = time.monotonic()

    for index, export_model in enumerate(export_models, 1):
        log.info("Starting %s export (%s/%s)", export_model.__name__, index, len(export_models))
        elements = exporter(export_model)
        save_to_file(export_model.export_file_path(output_directory), elements)
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


def download_file(source, output_directory: str = root_directory, alias_name: str = None):
    import urllib.request
    import re
    filename = alias_name if alias_name else re.search(r"[ \w-]+\.\w+$", source)[0]
    urllib.request.urlretrieve(source, f"{output_directory}{filename}")


if __name__ == "__main__":
    file = "https://raw.githubusercontent.com/torrua/LOD/master/tables/LexEvent.txt"
    download_file(file)
