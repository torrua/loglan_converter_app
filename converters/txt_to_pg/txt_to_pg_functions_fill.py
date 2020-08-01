# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from config import log, SEPARATOR, DEFAULT_LANGUAGE
from config.postgres import db, models_pg_from_file, models_pg_to_db
from config.postgres.model_dictionary import ComplexAuthor, ComplexEvent, \
    ComplexDefinition, ComplexSetting, ComplexSyllable, ComplexType, ComplexWord, ComplexWordSpell, ComplexKey
from converters.txt_to_pg.converters_txt_to_pg import converters_pg
from config.text.functions import download_dictionary_file
from config.text import IMPORT_DIRECTORY_PATH_LOCAL


def add_objects_to_db(model: str, converter, data: tuple) -> None:
    """
    Generate objects and save them to the Database
    :param model: Object's class name
    :param converter: Callable function to convert data
    :param data: Data imported from text file
    :return: None
    """
    log.info("Start to process %s objects", model)
    objects = converter(*data)
    log.info("Total number of %s objects - %s", model, len(objects))
    log.info("Add %s objects to Database", model)
    db.session.bulk_save_objects(objects)
    log.debug("Commit Database changes")
    db.session.commit()
    log.info("Finish to process %s objects\n", model)


def get_txt_dataset(source_path: str):
    """
    :param source_path:
    :return:
    """
    return {model.__name__: download_dictionary_file(
            url=f"{source_path}{model.import_file_name}", model_name=model.__name__)
            for model in models_pg_from_file}


def get_dataset_for_converters(source_path: str, language: str) -> dict:
    txt_dataset = get_txt_dataset(source_path)
    return {
        ComplexAuthor.__name__: (txt_dataset[ComplexAuthor.__name__],),
        ComplexEvent.__name__: (txt_dataset[ComplexEvent.__name__],),
        ComplexKey.__name__: (txt_dataset[ComplexDefinition.__name__], language),
        ComplexSetting.__name__: (txt_dataset[ComplexSetting.__name__],),
        ComplexSyllable.__name__: (txt_dataset[ComplexSyllable.__name__],),
        ComplexType.__name__: (txt_dataset[ComplexType.__name__],),
        ComplexWord.__name__: (txt_dataset[ComplexWord.__name__], txt_dataset[ComplexWordSpell.__name__]),
        ComplexDefinition.__name__: (txt_dataset[ComplexDefinition.__name__], language), }


def db_fill_tables(dataset: dict, converters: tuple = converters_pg, ) -> None:
    """
        Consecutively execute converters and send data to the database
    ! The execution order is important for at least the following data types:
        Type -> Word -> Definition,
    because the conversion of definitions depends on existing words,
    and the conversion of words depends on existing types
    :param dataset:
    :param converters:
    :return:
    """
    log.info("Start to fill tables with dictionary data")
    for converter, model_name, model_data in zip(converters, dataset.keys(), dataset.values()):
        log.info("Start to process %s objects", model_name)
        objects = converter(*model_data)
        log.info("Total number of %s objects - %s", model_name, len(objects))
        log.info("Add %s objects to Database", model_name)
        db.session.bulk_save_objects(objects)
        log.debug("Commit Database changes")
        db.session.commit()
        log.info("Finish to process %s objects\n", model_name)

    log.info("Finish to fill tables with dictionary data\n")
