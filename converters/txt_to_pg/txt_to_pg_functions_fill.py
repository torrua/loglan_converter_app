# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from config import log, SEPARATOR, DEFAULT_LANGUAGE
from config.postgres import db, models_pg_from_file, models_pg_to_db
from config.postgres.model_dictionary import Author, Event, \
    Definition, Setting, Syllable, Type, Word, WordSpell, Key
from converters.txt_to_pg.txt_to_pg_functions_convert import converters_pg
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
        Author.__name__: (txt_dataset[Author.__name__],),
        Event.__name__: (txt_dataset[Event.__name__],),
        Key.__name__: (txt_dataset[Definition.__name__], language),
        Setting.__name__: (txt_dataset[Setting.__name__],),
        Syllable.__name__: (txt_dataset[Syllable.__name__],),
        Type.__name__: (txt_dataset[Type.__name__],),
        Word.__name__: (txt_dataset[Word.__name__], txt_dataset[WordSpell.__name__]),
        Definition.__name__: (txt_dataset[Definition.__name__], language), }


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
