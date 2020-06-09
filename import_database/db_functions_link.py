# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""
Module for creating database relationships
"""

import re
from typing import List

from import_database import db, log, SEPARATOR
from import_database import Author, Word, Type, Definition, Key
from import_database.db_functions_import import download_dictionary_file


def _db_link_authors(words: List[List[str]]) -> None:
    """
    Create relations between words and their authors (WID <-> AID) in DB
    These connections locate in 't_connect_authors' table

    :param words: List of words' data received from a text file
        using function convert_file_to_list
    :return: None
    """
    log.info("Start to link words with their authors")

    all_authors = Author.query.all()
    author_by_abbr = {author.abbreviation: author for author in all_authors}

    # Get a dictionary with a list of abbreviations of authors of each word by key WID_old
    dict_of_authors_data_as_dict = {
        int(word_data[0]): word_data[5].split(" ", 1)[0].split("/")
        for word_data in words}

    for word in Word.query.all():
        authors_abbreviations = dict_of_authors_data_as_dict[word.id_old]
        # print(word) if not authors_abbreviations else None

        abbreviations = [
            word.add_author(author_by_abbr[abbreviation])
            for abbreviation in authors_abbreviations]
        log_text = f"{word.name} {' '*(26-len(word.name))}-> {'/'.join(abbreviations)}"
        log.debug(log_text)
    db.session.commit()
    log.info("Finish to link words with their authors")


def _db_link_complexes(words: List[List[str]]) -> None:
    """
    Create relations in DB between -
        primitives and derivative complexes,
        primitives and derivative small words,
        small words and combinations based on them
    :param words: List of words' data received from a text file
        using function convert_file_to_list
    :return: None
    """

    log.info("Start to create relations between primitives and their derivatives")

    def get_elements_from_str(set_as_str: str, separator: str = " | ") -> list:
        return [element.strip() for element in set_as_str.split(separator)]

    for item in words:
        if not item[10]:  # If 'Used In' field does not exist
            continue

        # On idea only one parent should always be here
        parents = Word.query.filter(Word.id_old == int(item[0])).all()
        if len(parents) > 1:
            log.warning(
                "The are %s for this word!\n%s",
                len(parents), [parent.name for parent in parents])
        for parent in parents:
            children = Word.query.filter(Word.name.in_(
                get_elements_from_str(item[10]))).order_by(Word.id.asc()).all()

            child_names = [parent.add_child(child) for child in children if child]
            # TODO There are unspecified words, for example, <zvovai>
            log_text = f"{parent.name} {' ' * (26 - len(parent.name))}-> {child_names}"
            log.debug(log_text)
    db.session.commit()
    log.info("Finish to create relations between primitives and their derivatives")


def _db_link_affixes(words: List[List[str]]) -> None:
    """
    Create relations in DB between primitives and their affixes
    :param words: List of words' data received from a text file
        using function convert_file_to_list
    :return: None
    """
    log.info("Start to link words with their affixes")

    def get_elements_from_str(set_as_str: str, separator: str = " ") -> list:
        return [element.strip() for element in set_as_str.split(separator)]

    for item in words:
        if not item[3]:
            continue

        djifoas_as_str = get_elements_from_str(item[3])

        djifoas_as_object = Word.query.join(Type) \
            .filter(Word.name.in_(djifoas_as_str)) \
            .filter(Type.type == "Afx").all()

        # there may be several parents if these are a language-people-culture primitives
        primitives = Word.query.join(Type) \
            .filter(Word.id_old == int(item[0])) \
            .filter(Type.group == "Prim").all()

        for prim in primitives:
            affix_names = [prim.add_child(djifoa) for djifoa in djifoas_as_object]
            log.debug("%s < %s", prim.name, affix_names)
    db.session.commit()
    log.info("Finish to link words with their affixes")


def _db_link_keys() -> None:
    """
    # Create relations in DB between definitions and their keys
    :return: None
    """
    log.info("Start to link definitions with their keys")
    pattern = r"(?<=\«)(.+?)(?=\»)"
    all_definitions = Definition.query.all()
    for definition in all_definitions:
        keys = re.findall(pattern, definition.body)
        log.debug("%s - %s: %s", definition.source_word.name, definition.position, keys)
        key_objects = Key.query.filter(Key.word.in_(keys)).all()
        _ = [definition.add_key(key) for key in key_objects]
    db.session.commit()
    log.info("Finish to link definitions with their keys")


def db_link_tables() -> None:
    """
    Link existing data between tables. For example,
        connect Word objects with Author object(s)
        connect primitives with their complexes (Word with Word)
        connect primitives with their affixes (Word with Word)
        connect Definitions object with their Key object(s)
    These links locate in according tables, like
        connect_authors, connect_words, connect_keys
    See Models module for more details about them
    :return: None
    """

    log.info("Start to link tables data")
    imported_words = download_dictionary_file("Word", SEPARATOR)
    _db_link_authors(imported_words)
    _db_link_complexes(imported_words)
    _db_link_affixes(imported_words)
    _db_link_keys()
    log.info("Finish to link tables data")
