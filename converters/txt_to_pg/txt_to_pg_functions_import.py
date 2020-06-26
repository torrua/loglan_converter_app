# -*- coding: utf-8 -*-
""""
Module for loading dictionary data from text files
"""

from typing import List
import requests

from config import log, SEPARATOR
from config.postgres.model_dictionary import models_pg as pg_import_models
from config.text import IMPORT_FILE_PATHS


def download_dictionary_file(model: str, separator: str = SEPARATOR) -> List[List[str]]:
    """
    Convert text file downloaded from the Github to the python list
        where each item is a list with line's elements
    :param model:
    :param separator: separation symbol, '@' by default
    :return: prepared python list
    """

    log.debug("Start to get '%s' content", model)
    model_names = [item.__name__ for item in pg_import_models]

    data = dict(zip(model_names, IMPORT_FILE_PATHS))
    url = data.get(model)
    print(data)
    if url.startswith("http"):
        lines = requests.get(url).text.split("\n")
    else:
        file = open(url, 'r')
        lines = file.read().split("\n")

    log.debug("Finish to get '%s' content\n", model)
    return [file_line.strip().split(separator) for file_line in lines if file_line]
