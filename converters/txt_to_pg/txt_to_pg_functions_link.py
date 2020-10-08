# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""
Module for creating database relationships
"""

from typing import List

from config import log
from config.postgres import db, app_lod
from config.postgres.models import Author, Type, Definition, Word


def db_link_authors(words: List[List[str]]) -> None:
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

    # Get a dictionary with a list of abbreviations of authors of each word by id_old
    dict_of_authors_data_as_dict = {
        int(word_data[0]): word_data[5].split(" ", 1)[0].split("/")
        for word_data in words}

    for word in Word.query.all():
        authors_abbreviations = dict_of_authors_data_as_dict[word.id_old]
        word.add_authors([author_by_abbr[abbreviation] for abbreviation in authors_abbreviations])
        log_text = f"{word.name} {' '*(26-len(word.name))}-> {'/'.join(authors_abbreviations)}"
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

    all_words = Word.get_all()
    all_word_names = [w.name for w in all_words]
    for item in words:
        if not item[10]:  # If 'Used In' field does not exist
            continue

        # On idea only one parent should always be here
        # parents = Word.query.filter(Word.id_old == int(item[0])).all()
        parents = [word for word in all_words if word.id_old == int(item[0])]  # LOCAL
        if len(parents) > 1:
            log.warning(
                "The are %s for this word!\n%s",
                len(parents), [parent.name for parent in parents])
        for parent in parents:
            child_names = get_elements_from_str(item[10])
            # children = Word.query.filter(Word.name.in_(child_names)).order_by(Word.id.asc()).all()
            children = [w for w in all_words if (w and (w.name in child_names))]  # LOCAL

            children = [child for child in children if child]
            # In case if any unspecified word exist in used_in list
            [log.debug(parent, child) for child in child_names if child not in all_word_names]

            parent.add_children(children)
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

    all_links_counter = 0

    for item in words:
        if not item[3]:
            continue

        djifoas_as_str = get_elements_from_str(item[3])
        djifoas_as_str_with_hyphen = [f"{affix}-" for affix in djifoas_as_str]
        djifoas = djifoas_as_str + djifoas_as_str_with_hyphen

        djifoas_as_object = Word.query.join(Type) \
            .filter(Word.name.in_(djifoas)) \
            .filter(Type.type == "Afx").all()

        all_links_counter += len(djifoas_as_object)

        primitive = Word.query.filter(Word.id_old == int(item[0])).first()
        primitive.add_children(djifoas_as_object)
        log.debug("%s < %s", primitive.name, djifoas_as_str)

    db.session.commit()

    log.info("Total number of links Word < Afx: %s", all_links_counter)
    log.info("Finish to link words with their affixes")


def db_link_keys() -> None:
    """
    # Create relations in DB between definitions and their keys
    :return: None
    """
    log.info("Start to link definitions with their keys")

    for definition in Definition.query.all():
        added_keys = definition.link_keys()
        log.debug(
            "%s - %s: %s", definition.source_word.name,
            definition.position, [k.word for k in added_keys] if added_keys else None)

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
    words_dataset = dataset[Word.__name__][0]
    log.info("Start to link tables data")
    db_link_authors(words_dataset)
    db_link_complexes(words_dataset)
    db_link_affixes(words_dataset)
    db_link_keys()
    log.info("Finish to link tables data")


if __name__ == "__main__":
    from config.postgres import CLIConfig

    with app_lod(CLIConfig).app_context():
        pass
