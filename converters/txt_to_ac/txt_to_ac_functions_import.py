# -*- coding: utf-8 -*-
""""
Module for loading dictionary data from text files
"""

from typing import List
import requests
import os

from config.access.model_dictionary import models_ac as ac_models

from config import log, SEPARATOR

IMPORT_DIRECTORY_PATH = os.getenv("IMPORT_DIRECTORY_PATH", None)


def download_dictionary_file(model: str, separator: str = SEPARATOR) -> List[List[str]]:
    """
    Convert text file downloaded from the Github to the python list
        where each item is a list with line's elements
    :param model:
    :param separator: separation symbol, '@' by default
    :return: prepared python list
    """

    log.debug("Start to get '%s' content", model)

    model_data = {item.__name__: f"{IMPORT_DIRECTORY_PATH}{item.import_file_name}" for item in ac_models}
    url = model_data.get(model)

    if str(url).startswith("http"):
        lines = requests.get(url).text.split("\n")
    else:
        file = open(url, 'r', encoding="utf-8")
        lines = file.read().split("\n")

    log.debug("Finish to get '%s' content\n", model)
    return [file_line.strip().split(separator) for file_line in lines if file_line]
