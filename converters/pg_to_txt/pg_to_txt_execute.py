# -*- coding: utf-8 -*-
# !/usr/bin/env python3

""""
Module for uploading data from Postgres database to text files
"""

from typing import List

from config import log
from config.postgres import EXPORT_PG_FILE_PATHS_LOCAL
from config.text.functions import convert_schema_to_txt
from converters.pg_to_txt.pg_model_export_to_txt import export_models_pg

# pylint: disable=E1101


def convert_model_to_txt(export_model) -> List[str]:
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
    export_schema = dict(zip(EXPORT_PG_FILE_PATHS_LOCAL, export_models_pg))
    export_suffix = "PG"
    convert_schema_to_txt(export_schema, convert_model_to_txt, export_suffix)


if __name__ == "__main__":
    convert_pg_to_txt()
