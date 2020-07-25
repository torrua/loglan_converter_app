# -*- coding: utf-8 -*-
""""Module for uploading data from AC database to PG database"""
from typing import List

from config import DEFAULT_LANGUAGE, SEPARATOR
from config.access import session, engine
from config.postgres.model_dictionary import Author, Event, \
    Key, Setting, Syllable, Type, Word, Definition
from config.access.ac_model_export_to_txt import IOAuthor, \
    IOEvent, IODefinition, IOSyllable, IOSetting, IOWord, \
    IOWordSpell, IOType
from converters.txt_to_pg.__init__ import generic_convert_to_pg


def convert_model_to_txt(export_model) -> List[List[str]]:
    """
    This convert function suitable for all AC models
    :param export_model: Flask_sqlalchemy.model.DefaultMeta object
    :return: List[str]
    """
    ac_session = session()
    if getattr(export_model, "word_id", False) and getattr(export_model, "type", False):
        collection = ac_session.query(export_model).order_by(
            export_model.word_id.asc()).all()
    elif getattr(export_model, "word_id", False) and getattr(export_model, "position", False):
        collection = ac_session.query(export_model).order_by(
            export_model.word_id.asc(), export_model.position.asc()).all()
    else:
        collection = ac_session.query(export_model).all()

    elements = list(dict.fromkeys([item.export() for item in collection]))
    ac_session.close()
    engine.dispose()
    return [item.strip().split(SEPARATOR) for item in elements]


def get_txt_dataset(language: str):
    return {
        Author.__name__: (convert_model_to_txt(IOAuthor),),
        Event.__name__: (convert_model_to_txt(IOEvent),),
        Key.__name__: (convert_model_to_txt(IODefinition), language,),
        Setting.__name__: (convert_model_to_txt(IOSetting),),
        Syllable.__name__: (convert_model_to_txt(IOSyllable),),
        Type.__name__: (convert_model_to_txt(IOType),),
        Word.__name__: (convert_model_to_txt(IOWord), convert_model_to_txt(IOWordSpell),),
        Definition.__name__: (convert_model_to_txt(IODefinition), language), }


def convert_ac_to_pg() -> None:
    dataset = get_txt_dataset(DEFAULT_LANGUAGE)
    generic_convert_to_pg(dataset=dataset)


if __name__ == "__main__":
    convert_ac_to_pg()
