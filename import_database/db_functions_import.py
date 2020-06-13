# -*- coding: utf-8 -*-
""""
Module for loading dictionary data from text files
"""

from os import environ
from typing import List
import requests

from import_database import log, SEPARATOR
from import_database import Author, Definition, Event, Setting, Syllable, Type, Word, WordSpell, XWord


def download_dictionary_file(model: str, separator: str = SEPARATOR) -> List[List[str]]:
    """
    Convert text file downloaded from the Github to the python list
        where each item is a list with line's elements
    :param model:
    :param separator: separation symbol, '@' by default
    :return: prepared python list
    """

    log.debug("Start to get '%s' content", model)
    classes = (Author, Definition, Event, Setting, Syllable, Type, Word, WordSpell, XWord,)
    models = [item.__name__ for item in classes]
    names_variables = [
        "FILE_NAME_AUTHOR", "FILE_NAME_WORDDEFINITION", "FILE_NAME_LEXEVENT",
        "FILE_NAME_SETTINGS", "FILE_NAME_PERMISSIBLEINITIALCC", "FILE_NAME_TYPE",
        "FILE_NAME_WORDS", "FILE_NAME_WORDSPELL", "FILE_NAME_XWORD", ]

    data = {model_name: file_name for model_name, file_name in zip(models, names_variables)}
    file_name = environ.get(data.get(model))

    directory_path = environ.get('IMPORT_DIRECTORY_PATH')
    url = f"{directory_path}{file_name}"
    lines = requests.get(url).text.split("\n")
    log.debug("Finish to get '%s' content", model)

    return [file_line.strip().split(separator) for file_line in lines if file_line]


def db_get_statistic(db_models: list):
    """

    :param db_models:
    :return:
    """
    # TODO
    log.info("Start to get statistic of imported items:")
    for model in db_models:
        log.info(f"{model.__name__}: {model.query.count()}")
    log.info("Finish to get statistic of imported items")
