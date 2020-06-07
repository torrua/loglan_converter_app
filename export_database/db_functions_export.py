# -*- coding: utf-8 -*-
""""
Модуль для выгрузки данных из базы данных в текстовые файлы
"""

from os import path, makedirs
from typing import List

from export_database import log, EXPORT_DIRECTORY_PATH, EXPORT_FILE_NAME_AUTHOR, \
    EXPORT_FILE_NAME_LEXICAL_EVENT, EXPORT_FILE_NAME_PERMISSIBLE_INITIAL_CC, \
    EXPORT_FILE_NAME_SETTINGS, EXPORT_FILE_NAME_TYPE, EXPORT_FILE_NAME_WORD_DEFINITION, \
    EXPORT_FILE_NAME_WORDS, EXPORT_FILE_NAME_WORD_SPELL

from export_database.model_dictionary_export import ExportAuthor, ExportEvent, \
    ExportSyllable, ExportSetting, ExportType, ExportWord, ExportDefinition

# pylint: disable=E1101


def extractor_default(collection) -> List[str]:
    """
    Extract object's data for exporting
    :param collection: List of objects to export
    :return: List of object's data as string
    """
    return list(dict.fromkeys([item.export() for item in collection]))


def extractor_spell(collection) -> List[str]:
    """
    Extract object's data for exporting
    :param collection: List of objects to export
    :return: List of object's data as string
    """
    return list(dict.fromkeys([item.export_spell_as_string for item in collection]))


def export_to_file(data_object, file_path: str, extractor) -> None:
    """
    This export function suitable for all types of data
    :param data_object: Flask_sqlalchemy.model.DefaultMeta object
    :param file_path: Full path for export file
    :param extractor: Function with rules how to extract
    :return: None
    """
    log.info("Starting %s export", data_object.__name__)

    attr = getattr(data_object, "id_old", None)
    if attr:
        collection = data_object.query.order_by(data_object.id_old.asc()).all()
    else:
        collection = data_object.query.all()

    log.debug("%s items imported from database", len(collection))
    log.debug("Preparing imported items to export")
    elements = sorted(extractor(collection))
    log.debug("%s unique items ready to export", len(elements))

    all_items = []
    for element in elements:
        all_items.append(element)
        all_items.append("\n")

    with open(file_path, "w+", encoding="utf-8") as file:
        for element in all_items[:-1]:
            file.write(element)
    file.close()

    with open(file_path, "rb") as file:
        exported_amount = len([line for line in file if line])
    file.close()

    log.debug("%s items exported to %s", exported_amount, file_path.replace(r"\\", '\\'))
    log.info("Ending %s export\n", data_object.__name__)


def export_db():
    """

    :return:
    """
    log.info("Starting db export")

    export_data = {
        EXPORT_FILE_NAME_AUTHOR: (ExportAuthor, extractor_default),
        EXPORT_FILE_NAME_LEXICAL_EVENT: (ExportEvent, extractor_default),
        EXPORT_FILE_NAME_PERMISSIBLE_INITIAL_CC: (ExportSyllable, extractor_default),
        EXPORT_FILE_NAME_SETTINGS: (ExportSetting, extractor_default),
        EXPORT_FILE_NAME_TYPE: (ExportType, extractor_default),
        EXPORT_FILE_NAME_WORD_DEFINITION: (ExportDefinition, extractor_default),
        EXPORT_FILE_NAME_WORDS: (ExportWord, extractor_default),
        EXPORT_FILE_NAME_WORD_SPELL: (ExportWord, extractor_spell), }

    if not path.isdir(EXPORT_DIRECTORY_PATH):
        log.debug("Creating export directory: %s", EXPORT_DIRECTORY_PATH)
        makedirs(EXPORT_DIRECTORY_PATH)

    for key, value in export_data.items():
        export_to_file(value[0], key, value[1])

    log.info("Ending db export\n")


if __name__ == "__main__":
    export_db()
