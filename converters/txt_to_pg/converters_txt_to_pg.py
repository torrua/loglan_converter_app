# -*- coding: utf-8 -*-
"""
Module for converting data from text files to a database
"""

import ast
import re
from datetime import datetime
from typing import List
from config import log
from config.postgres.model_base import Author, Event, \
    Definition, Setting, Syllable, Type, Word, Key


def converter_authors(authors: List[List[str]]) -> List[Author]:
    """
    Convert authors' txt data to DB objects
    :param authors: List of authors received from a text file
        using function convert_file_to_list
    :return: List of Author object(s)
    """
    return [Author(**{
        "abbreviation": item[0],
        "full_name": item[1],
        "notes": item[2]})
            for item in authors]


def converter_events(events: List[List[str]]) -> List[Event]:
    """
    Convert events' data (dictionary versions) to DB objects
    :param events: List of events received from a text file
        using function convert_file_to_list
    :return: List of Event object(s)
    """
    return [Event(**{
        "id": int(item[0]),
        "date": datetime.strptime(item[2], '%m/%d/%Y'),
        "name": item[1],
        "definition": item[3],
        "annotation": item[4],
        "suffix": item[5],
    }) for item in events]


def converter_settings(settings: List[List[str]]) -> List[Setting]:
    """
    Convert settings' data to DB objects
    :param settings: List of settings sets received from a text file
        using function convert_file_to_list
    :return: List of Setting object(s)
    """
    return [Setting(**{
        "date": datetime.strptime(item[0], '%d.%m.%Y %H:%M:%S'),
        "db_version": int(item[1]),
        "last_word_id": int(item[2]),
        "db_release": item[3],
    }) for item in settings]


def converter_syllables(syllables: List[List[str]]) -> List[Syllable]:
    """
    Convert syllables' data to DB objects
    :param syllables: List of syllables received from a text file
        using function convert_file_to_list
    :return: List of Syllable object(s)
    """
    return [Syllable(**{
        "name": item[0],
        "type": item[1],
        "allowed": ast.literal_eval(item[2]),
    }) for item in syllables]


def converter_types(types: List[List[str]]) -> List[Type]:
    """
    Convert words types' data to DB objects
    :param types: List of words types received from a text file
        using function convert_file_to_list
    :return: List of Type object(s)
    """
    return [Type(**{
        "type": item[0],
        "type_x": item[1],
        "group": item[2],
        "parentable": ast.literal_eval(item[3]),
        "description": item[4],
    }) for item in types]


def converter_words(words: List[List[str]], spell: List[List[str]]) -> List[Word]:
    """
    Convert words' data to DB objects
    ! This process requires that Type objects were already added to DB
    :param words: List of words' data received from a text file
        using function convert_file_to_list
    :param spell: List of words versioning by events (see Event description)
        received from a text file using function convert_file_to_list
    :return: List of Word object(s)
    """

    def get_year(str_date: str) -> dict:
        date_year = str_date.split(" ", 1)
        return {"year": datetime.strptime(date_year[0], "%Y").date(),
                "notes": date_year[1] if len(date_year) > 1 else None}

    def get_rank(str_rank: str) -> dict:
        rank_data = str_rank.split(" ", 1)
        return {"rank": rank_data[0],
                "notes": rank_data[1] if len(rank_data) > 1 else None}

    def get_author(str_author) -> dict:
        author_data = str_author.split(" ", 1)
        return {"author": author_data[0],
                "notes": author_data[1] if len(author_data) > 1 else None}

    def get_notes(item: list) -> dict:
        str_notes = {}
        author = get_author(item[5])["notes"]
        year = get_year(item[6])["notes"]
        rank = get_rank(item[7])["notes"]

        if author is not None:
            str_notes["author"] = author
        if year is not None:
            str_notes["year"] = year
        if rank is not None:
            str_notes["rank"] = rank

        return str_notes if str_notes else None

    types = dict((item.type, item.id) for item in Type.query.all())

    dict_of_word_names_as_dict = {(index, int(item[0])): {
        "name": item[1],
        "id_old": int(item[0]),
        "event_start_id": int(item[4]),
        "event_end_id": int(item[5]) if int(item[5]) < 9999 else None
    } for index, item in enumerate(spell)}

    dict_of_word_data_as_dict = {int(item[0]): {
        "authors": get_author(item[5])["author"],
        "type_id": types[item[1]],
        "origin": item[8],
        "origin_x": item[9],
        "id_old": int(item[0]),
        "match": item[4],
        "rank": get_rank(item[7])["rank"],
        "year": get_year(item[6])["year"],
        "TID_old": int(item[11]) if item[11] else None,
        "notes": get_notes(item),
    } for item in words}

    dowdad = dict_of_word_data_as_dict
    downad = dict_of_word_names_as_dict

    words = [Word(**{
        "name": downad[index]["name"],
        "event_start_id": downad[index]["event_start_id"],
        "event_end_id": downad[index]["event_end_id"],
        "id_old": dowdad[index[1]]["id_old"],
        "origin": dowdad[index[1]]["origin"],
        "origin_x": dowdad[index[1]]["origin_x"],
        "type_id": dowdad[index[1]]["type_id"],
        "match": dowdad[index[1]]["match"],
        "rank": dowdad[index[1]]["rank"],
        "year": dowdad[index[1]]["year"],
        "notes": dowdad[index[1]]["notes"],
        "TID_old": dowdad[index[1]]["TID_old"]
    }) for index in downad.keys()]

    words.sort(key=lambda x: x.name)
    return words


def converter_definitions(
        definitions: List[List[str]], language: str) -> List[Definition]:
    """
    Convert words definitions' data to DB objects
    :param definitions: List of definitions received from a text file
        using function convert_file_to_list
    :param language: Definitions' language
    :return: List of Definition object(s)
    """
    def get_grammar(str_grammar: str) -> dict:
        slots = re.search(r"\d", str_grammar)
        code = re.search(r"\D+", str_grammar)

        return {
            "slots": int(slots.group(0)) if slots else None,
            "code": code.group(0) if code else "", }

    all_definitions = []
    for item in definitions:
        for word in Word.query.filter(Word.id_old == int(item[0])).all():
            all_definitions.append(Definition(**{
                "word_id": word.id,
                "position": int(item[1]),
                "usage": item[2],
                "slots": get_grammar(item[3])["slots"],
                "grammar_code": get_grammar(item[3])["code"],
                "body": item[4],
                "language": language,
                "case_tags": item[6],
            }))
    return all_definitions


def converter_keys(
        definitions: List[List[str]], language: str) -> List[Key]:
    """
    Convert all unique keys received from words' definitions to DB objects
    :param definitions: List of definitions received from a text file
        using function convert_file_to_list
    :param language: Keys' language
    :return: List with Key object(s)
    """
    log.info("Start collecting dictionary keys")

    def dict_from_word_definition(wd_line: List[str]) -> dict:
        """
        Create python dict from file's line
        :param wd_line: file's line as list of str
        :return: dict with keys: "WID", "position", "usage", "grammar_code", "body", "case_tags"
        """
        keys = ("id_old", "position", "usage", "grammar_code", "body", "case_tags", )
        return dict(zip(keys, wd_line))

    def keys_from_string(string: str) -> List[str]:
        key_pattern = r"(?<=\«)(.+?)(?=\»)"
        return re.findall(key_pattern, string)

    all_keys = []
    without_keys_count = 0

    for definition_line in definitions:
        body = dict_from_word_definition(definition_line)["body"]
        keys_from_line = keys_from_string(body)

        if not keys_from_line:
            without_keys_count += 1
        else:
            all_keys.extend(keys_from_line)

    unique_keys = sorted(set(all_keys))

    log.info("Total number of keys:\t\t%s", len(all_keys))
    log.info("Unique keys from all:\t\t%s", len(unique_keys))
    if without_keys_count:
        log.warning("Definitions without keys:\t%s", without_keys_count)
    log.info("Finish collecting dictionary keys\n")

    return [Key(**{"word": key, "language": language, }) for key in unique_keys]


converters_pg = (
    converter_authors, converter_events, converter_keys, converter_settings,
    converter_syllables, converter_types, converter_words, converter_definitions, )
