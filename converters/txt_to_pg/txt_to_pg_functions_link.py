# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""
Module for creating database relationships
"""

import re
from typing import List

from config import log
from config.postgres import db
from config.postgres.model_dictionary import ComplexAuthor, ComplexDefinition, ComplexType, ComplexWord, ComplexKey


def db_link_authors(words: List[List[str]]) -> None:
    """
    Create relations between words and their authors (WID <-> AID) in DB
    These connections locate in 't_connect_authors' table

    :param words: List of words' data received from a text file
        using function convert_file_to_list
    :return: None
    """
    log.info("Start to link words with their authors")

    all_authors = ComplexAuthor.query.all()
    author_by_abbr = {author.abbreviation: author for author in all_authors}

    # Get a dictionary with a list of abbreviations of authors of each word by id_old
    dict_of_authors_data_as_dict = {
        int(word_data[0]): word_data[5].split(" ", 1)[0].split("/")
        for word_data in words}

    for word in ComplexWord.query.all():
        authors_abbreviations = dict_of_authors_data_as_dict[word.id_old]

        abbreviations = [
            word.add_author(author_by_abbr[abbreviation])
            for abbreviation in authors_abbreviations]
        log_text = f"{word.name} {' '*(26-len(word.name))}-> {'/'.join(abbreviations)}"
        log.debug(log_text)
    db.session.commit()
    log.info("Finish to link words with their authors")


def db_link_complexes(words: List[List[str]]) -> None:
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
        parents = ComplexWord.query.filter(ComplexWord.id_old == int(item[0])).all()
        if len(parents) > 1:
            log.warning(
                "The are %s for this word!\n%s",
                len(parents), [parent.name for parent in parents])
        for parent in parents:
            children = ComplexWord.query.filter(ComplexWord.name.in_(
                get_elements_from_str(item[10]))).order_by(ComplexWord.id.asc()).all()

            child_names = [parent.add_child(child) for child in children if child]
            # TODO There are unspecified words, for example, <zvovai>

            log_text = f"{parent.name} {' ' * (26 - len(parent.name))}-> {child_names}"
            log.debug(log_text)
    db.session.commit()
    log.info("Finish to create relations between primitives and their derivatives")


def db_link_affixes(words: List[List[str]]) -> None:
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
        djifoas_as_str_with_hyphen = [f"{affix}-" for affix in djifoas_as_str]
        djifoas = djifoas_as_str + djifoas_as_str_with_hyphen

        djifoas_as_object = ComplexWord.query.join(ComplexType) \
            .filter(ComplexWord.name.in_(djifoas)) \
            .filter(ComplexType.type == "Afx").all()

        # there may be several parents if these are a language-people-culture primitives
        primitives = ComplexWord.query.join(ComplexType) \
            .filter(ComplexWord.id_old == int(item[0])) \
            .filter(ComplexType.group == "Prim").all()

        for prim in primitives:
            affix_names = [prim.add_child(djifoa) for djifoa in djifoas_as_object]
            log.debug("%s < %s", prim.name, affix_names)
    db.session.commit()
    log.info("Finish to link words with their affixes")


def db_link_keys() -> None:
    """
    # Create relations in DB between definitions and their keys
    :return: None
    """
    log.info("Start to link definitions with their keys")
    pattern = r"(?<=\«)(.+?)(?=\»)"
    all_definitions = ComplexDefinition.query.all()
    for definition in all_definitions:
        keys = re.findall(pattern, definition.body)
        log.debug("%s - %s: %s", definition.source_word.name, definition.position, keys)
        key_objects = ComplexKey.query.filter(ComplexKey.word.in_(keys)).all()
        _ = [definition.add_key(key) for key in key_objects]
    db.session.commit()
    log.info("Finish to link definitions with their keys")


def db_link_tables(dataset: dict) -> None:
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
    words_dataset = dataset[ComplexWord.__name__][0]
    log.info("Start to link tables data")
    db_link_authors(words_dataset)
    db_link_complexes(words_dataset)
    db_link_affixes(words_dataset)
    db_link_keys()
    log.info("Finish to link tables data")
