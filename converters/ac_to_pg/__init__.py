# -*- coding: utf-8 -*-
""""Module for uploading data from AC database to PG database"""
from typing import List

from config import DEFAULT_LANGUAGE, SEPARATOR
from config.access import ac_session
from config.postgres.model_dictionary import Author, Event, \
    Key, Setting, Syllable, Type, Word, Definition
from converters.ac_to_txt.ac_model_export_to_txt import ExportAuthor, \
    ExportEvent, ExportDefinition, ExportSyllable, ExportSetting, ExportWord, \
    ExportWordSpell, ExportType
from converters.txt_to_pg.__init__ import generic_convert_to_pg


def convert_model_to_txt(export_model) -> List[List[str]]:
    """
    This convert function suitable for all AC models
    :param export_model: Flask_sqlalchemy.model.DefaultMeta object
    :return: List[str]
    """
    if getattr(export_model, "word_id", False) and getattr(export_model, "type", False):
        collection = ac_session.query(export_model).order_by(
            export_model.word_id.asc()).all()
    elif getattr(export_model, "word_id", False) and getattr(export_model, "position", False):
        collection = ac_session.query(export_model).order_by(
            export_model.word_id.asc(), export_model.position.asc()).all()
    else:
        collection = ac_session.query(export_model).all()

    elements = list(dict.fromkeys([item.export() for item in collection]))
    return [item.strip().split(SEPARATOR) for item in elements]


def get_txt_dataset(language: str):
    return {
        Author.__name__: (convert_model_to_txt(ExportAuthor),),
        Event.__name__: (convert_model_to_txt(ExportEvent),),
        Key.__name__: (convert_model_to_txt(ExportDefinition), language,),
        Setting.__name__: (convert_model_to_txt(ExportSetting),),
        Syllable.__name__: (convert_model_to_txt(ExportSyllable),),
        Type.__name__: (convert_model_to_txt(ExportType),),
        Word.__name__: (convert_model_to_txt(ExportWord), convert_model_to_txt(ExportWordSpell),),
        Definition.__name__: (convert_model_to_txt(ExportDefinition), language), }


def convert_ac_to_pg() -> None:
    dataset = get_txt_dataset(DEFAULT_LANGUAGE)
    generic_convert_to_pg(dataset=dataset)


if __name__ == "__main__":
    convert_ac_to_pg()
