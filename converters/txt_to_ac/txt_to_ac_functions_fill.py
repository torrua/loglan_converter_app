# -*- coding: utf-8 -*-
""""
Module for adding dictionary data to the database
"""

from config import log
from config.access import ac_session, models_ac
from config.text.functions import download_dictionary_file
from converters.txt_to_ac.txt_to_ac_functions_convert import converters_ac


def db_fill_tables(
        source_path: str,
        models: list = models_ac,
        converters: tuple = converters_ac) -> None:
    """
    Consecutively execute converters and send data to the database
    ! The execution order is important for at least the following data types:
        Type -> Word -> Definition,
    because the conversion of definitions depends on existing words,
    and the conversion of words depends on existing types
    :param source_path:
    :param models:
    :param converters:
    :return:
    """
    log.info("Start to fill tables with dictionary data")
    for model, converter in zip(models, converters):

        model_name = model.__name__
        url = f"{source_path}{model.import_file_name}"

        data = download_dictionary_file(url, model_name)
        log.info("Start to process %s objects", model_name)
        objects = converter(data)
        log.info("Total number of %s objects - %s", model_name, len(objects))
        log.info("Add %s objects to Database", model_name)
        ac_session.bulk_save_objects(objects)
        log.debug("Commit Database changes")
        ac_session.commit()
        log.info("Finish to process %s objects\n", model_name)

    log.info("Finish to fill tables with dictionary data\n")
