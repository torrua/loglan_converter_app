# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from config import log, SEPARATOR
from config.postgres import db
from config.postgres.model_dictionary import Author, Event, \
    Definition, Setting, Syllable, Type, Word, WordSpell
from converters.txt_to_pg.txt_to_pg_functions_convert import converters
from converters.txt_to_pg.txt_to_pg_functions_import import download_dictionary_file


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


def get_txt_dataset(language: str):
    """
    :param language:
    :return:
    """
    return (
        (download_dictionary_file(Author.__name__),),
        (download_dictionary_file(Event.__name__),),
        (download_dictionary_file(Definition.__name__), language,),
        (download_dictionary_file(Setting.__name__),),
        (download_dictionary_file(Syllable.__name__),),
        (download_dictionary_file(Type.__name__),),
        (download_dictionary_file(Word.__name__), download_dictionary_file(WordSpell.__name__, SEPARATOR),),
        (download_dictionary_file(Definition.__name__), language),)


def db_fill_tables(dataset: tuple) -> None:
    """
    Consecutively execute converters and send data to the database
    ! The execution order is important for at least the following data types:
        Type -> Word -> Definition,
    because the conversion of definitions depends on existing words,
    and the conversion of words depends on existing types
    :param dataset:
    :return: None
    """
    log.info("Start to fill tables with dictionary data")

    ordered_models = [
        converter.__name__.replace("converter_", "").capitalize()
        for converter in converters]

    for model, converter, data in zip(ordered_models, converters, dataset):
        log.info("Start to process %s objects", model)
        objects = converter(*data)
        log.info("Total number of %s objects - %s", model, len(objects))
        log.info("Add %s objects to Database", model)
        db.session.bulk_save_objects(objects)
        log.debug("Commit Database changes")
        db.session.commit()
        log.info("Finish to process %s objects\n", model)

    log.info("Finish to fill tables with dictionary data\n")
