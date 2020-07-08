# -*- coding: utf-8 -*-
# !/usr/bin/env python3

""""
Module for uploading data from Postgres database to text files
"""

from typing import List

from config import log
from config.postgres import EXPORT_PG_DIRECTORY_PATH_LOCAL
from config.text.functions import convert_db_to_txt
from converters.pg_to_txt.pg_model_export_to_txt import export_models_pg

# pylint: disable=E1101


def export_pg_model_to_list_of_str(export_model) -> List[str]:
    """
    This convert function suitable for all PG models
    :param export_model: Flask_sqlalchemy.model.DefaultMeta object
    :return: List[str]
    """

    attr = getattr(export_model, "id_old", None)
    if attr:
        collection = export_model.query.order_by(
            export_model.id_old.asc(), export_model.name.asc()).all()
    else:
        collection = export_model.query.order_by(export_model.id.asc()).all()

    log.debug("%s items imported from database", len(collection))
    log.debug("Preparing imported items to export")
    elements = list(dict.fromkeys([item.export() for item in collection]))
    log.debug("%s unique items ready to export", len(elements))
    return elements


def convert_pg_to_txt():
    """A wrapper for converting an Access database into text files"""
    convert_db_to_txt(export_models_pg, export_pg_model_to_list_of_str, EXPORT_PG_DIRECTORY_PATH_LOCAL)


if __name__ == "__main__":
    convert_pg_to_txt()
