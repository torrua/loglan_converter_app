# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from converters.txt_to_ac.txt_to_ac_functions_convert import converters
from converters.txt_to_ac.txt_to_ac_functions_import import download_dictionary_file
from config.access import ac_session
from config.access.model_dictionary import models_ac
from config import log


def db_fill_tables() -> None:
    """
    Consecutively execute converters and send data to the database
    ! The execution order is important for at least the following data types:
        Type -> Word -> Definition,
    because the conversion of definitions depends on existing words,
    and the conversion of words depends on existing types
    :return: None
    """
    log.info("Start to fill tables with dictionary data")

    for model, converter in zip(models_ac, converters):
        model_name = model.__name__
        data = download_dictionary_file(model_name)
        log.info("Start to process %s objects", model_name)
        objects = converter(data)
        log.info("Total number of %s objects - %s", model_name, len(objects))
        log.info("Add %s objects to Database", model_name)
        ac_session.bulk_save_objects(objects)
        log.debug("Commit Database changes")
        ac_session.commit()
        log.info("Finish to process %s objects\n", model_name)

    log.info("Finish to fill tables with dictionary data\n")
