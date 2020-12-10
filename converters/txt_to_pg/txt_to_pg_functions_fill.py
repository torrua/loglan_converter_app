# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from loglan_db import db

from config import log
from config.postgres.models import Author, Event, Key, Setting, Syllable, \
    Type, Definition, Word, WordSpell, all_models_pg
from config.text.functions import download_dictionary_file
from converters.txt_to_pg.converters_txt_to_pg import converters_pg


def get_txt_dataset(source_path: str):
    """
    :param source_path:
    :return:
    """
    return {model.__name__: download_dictionary_file(
            url=f"{source_path}{model.file_name}", model_name=model.__name__)
            for model in all_models_pg if model.__load_from_file__}


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
