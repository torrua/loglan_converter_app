# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""
from import_database import Author, Event, Definition, Setting, Syllable, Type, Word, Key, WordSpell
from import_database import db, log, SEPARATOR

from import_database.db_functions_convert import converter_authors, \
    converter_events, converter_keys, converter_settings, converter_syllables, \
    converter_types, converter_words, converter_definitions

from import_database.db_functions_import import download_dictionary_file


def add_objects_to_db(model: str, converter, data: tuple) -> None:
    """
    Generate objects and save them to the Database
    :param model: Object's class name
    :param converter: Callable function to convert data
    :param data: Data imported from text file
    :return: None
    """
    log.debug("Start to process %s objects", model)
    objects = converter(*data)
    log.debug("Total number of %s objects - %s",
              model, len(objects))
    log.debug("Add %s objects to Database", model)
    db.session.bulk_save_objects(objects)
    log.debug("Commit Database changes")
    db.session.commit()
    log.debug("Finish to process %s objects\n", model)


def db_fill_tables(language: str) -> None:
    """
    Consecutively execute converters and send data to the database
    ! The execution order is important for at least the following data types:
        Type -> Word -> Definition,
    because the conversion of definitions depends on existing words,
    and the conversion of words depends on existing types
    :param language:
    :return: None
    """
    log.debug("Start to fill tables with dictionary data")

    models = (Author, Event, Key, Setting, Syllable, Type, Word, Definition, )

    converters = (converter_authors, converter_events, converter_keys, converter_settings,
                  converter_syllables, converter_types, converter_words, converter_definitions, )

    data_sets_for_converters = (
        (download_dictionary_file(Author.__name__),),
        (download_dictionary_file(Event.__name__),),
        (download_dictionary_file(Definition.__name__), language,),
        (download_dictionary_file(Setting.__name__),),
        (download_dictionary_file(Syllable.__name__),),
        (download_dictionary_file(Type.__name__),),
        (download_dictionary_file(Word.__name__), download_dictionary_file(WordSpell.__name__, SEPARATOR),),
        (download_dictionary_file(Definition.__name__), language), )

    for model, converter, data in zip(models, converters, data_sets_for_converters):
        add_objects_to_db(model.__name__, converter, data)

    log.debug("Finish to fill tables with dictionary data\n")
