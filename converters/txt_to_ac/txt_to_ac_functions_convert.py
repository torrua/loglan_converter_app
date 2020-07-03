# -*- coding: utf-8 -*-
"""
Module for converting data from text files to a database
"""

import ast
from datetime import datetime
from typing import List
from config.access.model_dictionary import AccessAuthor, AccessWordSpell, \
    AccessWord, AccessType, AccessDefinition, \
    AccessSetting, AccessSyllable, AccessEvent


def converter_authors(authors: List[List[str]]) -> List[AccessAuthor]:
    """
    Convert authors' txt data to DB objects
    :param authors: List of authors received from a text file
        using function convert_file_to_list
    :return: List of Author object(s)
    """
    return [AccessAuthor(**{
        "abbreviation": item[0],
        "full_name": item[1] if item[1] else None,
        "notes": item[2] if item[2] else None})
            for item in authors]


def converter_events(events: List[List[str]]) -> List[AccessEvent]:
    """
    Convert events' data (dictionary versions) to DB objects
    :param events: List of events received from a text file
        using function convert_file_to_list
    :return: List of Event object(s)
    """
    return [AccessEvent(**{
        "id": int(item[0]),
        "name": item[1],
        "date": item[2],
        "definition": item[3],
        "annotation": item[4] if item[4] else None,
        "suffix": item[5] if item[5] else None,
    }) for item in events]


def converter_settings(settings: List[List[str]]) -> List[AccessSetting]:
    """
    Convert settings' data to DB objects
    :param settings: List of settings sets received from a text file
        using function convert_file_to_list
    :return: List of Setting object(s)
    """
    return [AccessSetting(**{
        "date": datetime.strptime(item[0], '%d.%m.%Y %H:%M:%S'),
        "db_version": int(item[1]),
        "last_word_id": int(item[2]),
        "db_release": item[3],
    }) for item in settings]


def converter_syllables(
        syllables: List[List[str]]) -> List[AccessSyllable]:
    """
    Convert syllables' data to DB objects
    :param syllables: List of syllables received from a text file
        using function convert_file_to_list
    :return: List of Syllable object(s)
    """
    return [AccessSyllable(**{
        "name": item[0],
        "type": item[1],
        "allowed": ast.literal_eval(item[2]) if item[2] else False,
    }) for item in syllables]


def converter_types(types: List[List[str]]) -> List[AccessType]:
    """
    Convert words types' data to DB objects
    :param types: List of words types received from a text file
        using function convert_file_to_list
    :return: List of Type object(s)
    """
    return [AccessType(**{
        "type": item[0],
        "type_x": item[1],
        "group": item[2] if item[2] else None,
        "parentable": ast.literal_eval(item[3]),
    }) for item in types]


def converter_words(words: List[List[str]]) -> List[AccessWord]:
    """
    Convert words' data to DB objects
    ! This process requires that Type objects were already added to DB
    :param words: List of words' data received from a text file
        using function convert_file_to_list
        received from a text file using function convert_file_to_list
    :return: List of Word object(s)
    """
    return [AccessWord(**{
        "word_id": int(item[0]),
        "type": item[1],
        "type_x": item[2],
        "affixes": item[3] if item[3] else None,
        "match": item[4] if item[4] else None,
        "authors": item[5] if item[5] else None,
        "year": item[6] if item[6] else None,
        "rank": item[7] if item[7] else None,
        "origin": item[8] if item[8] else None,
        "origin_x": item[9] if item[9] else None,
        "used_in": item[10] if item[10] else None,
        "TID_old": int(item[11]) if item[11] else None,
    }) for item in words]


def converter_spell(words: List[List[str]]) -> List[AccessWordSpell]:
    """
    :param words:
    :return:
    """
    return [AccessWordSpell(**{
        "word_id": int(item[0]),
        "word": item[1],
        "sort_a": item[2],
        "sort_b": item[3],
        "event_start_id": int(item[4]),
        "event_end_id": int(item[5]),
        "origin_x": item[6] if item[6] else None,
    }) for item in words]


def converter_definitions(
        definitions: List[List[str]]) -> List[AccessDefinition]:
    """
    Convert words definitions' data to DB objects
    :param definitions: List of definitions received from a text file
        using function convert_file_to_list
    :return: List of Definition object(s)
    """

    return [AccessDefinition(**{
        "word_id": int(item[0]),
        "position": int(item[1]),
        "usage": item[2] if item[2] else None,
        "grammar": item[3] if item[3] else None,
        "body": item[4],
        "main": item[5] if item[5] else None,
        "case_tags": item[6] if item[6] else None,
    }) for item in definitions]


converters_ac = (
    converter_authors, converter_definitions, converter_events,
    converter_settings, converter_syllables, converter_types,
    converter_words, converter_spell, )
