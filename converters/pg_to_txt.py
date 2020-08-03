# -*- coding: utf-8 -*-
# !/usr/bin/env python3

""""
Module for uploading data from Postgres database to text files
"""

from typing import List

from config import log
from config.text import EXPORT_DIRECTORY_PATH_LOCAL
from config.text.functions import convert_db_to_txt
from config.postgres.model_export import export_models_pg

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


def convert_pg_to_txt(output_directory: str = EXPORT_DIRECTORY_PATH_LOCAL):
    """A wrapper for converting a Postgres database into text files"""
    convert_db_to_txt(
        export_models=export_models_pg,
        exporter=export_pg_model_to_list_of_str,
        output_directory=output_directory)


if __name__ == "__main__":
    convert_pg_to_txt()
