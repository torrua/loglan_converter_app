# -*- coding: utf-8 -*-
# !/usr/bin/env python3

""""
Module for uploading data from Access database to text files
"""

from typing import List

from config import log
from config.access import ac_session
from converters.ac_to_txt.ac_model_export_to_txt import export_models_ac
from config.text import EXPORT_FILE_PATHS
from config.text.functions import convert_schema_to_txt

# pylint: disable=E1101


def convert_model_to_txt(export_model) -> List[str]:
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

    log.debug("%s items imported from database", len(collection))
    log.debug("Preparing imported items to export")
    elements = [item.export() for item in collection]
    log.debug("%s unique items ready to export", len(elements))
    return elements


def convert_ac_to_txt():
    """A wrapper for converting an Postgres database into text files"""
    export_schema = dict(zip(EXPORT_FILE_PATHS, export_models_ac))
    export_suffix = "AC"
    convert_schema_to_txt(export_schema, convert_model_to_txt, export_suffix)
