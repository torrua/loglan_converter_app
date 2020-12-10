# -*- coding: utf-8 -*-
"""
Module for check database data
"""

import re

from sqlalchemy import any_

from config import log
from config.postgres.models import Syllable, Type, Definition, Word


def check_tag_match(extended_result: bool = False):
    """
    Determine the discrepancy between the declared tags
    and those actually specified in the Definition
    :param extended_result: If True, returns an expanded dataset instead of a boolean
    :return: Boolean or tuple, depending on the extended_result variable
    """
    definitions = Definition.query.filter(Definition.case_tags != "").all()
    for defin in definitions:

        pattern_case_tags = f"[{''.join(Definition.APPROVED_CASE_TAGS)}]"
        list_tags = re.findall(pattern_case_tags, defin.case_tags)
        list_body = [tag for tag in re.findall(r'\w+', defin.body)
                     if tag in Definition.APPROVED_CASE_TAGS]

        result = list_tags == list_body

        if result:
            continue

        if extended_result:
            # print(df.source_word.name, result, list_tags, list_body)
            if len(defin.source_word.definitions.all()) > 1 and not list_body:
                second = f"\n\t{defin.source_word.definitions[1].grammar}" \
                         f" {defin.source_word.definitions[1].body}"
            else:
                second = ""
            print(f"{defin.source_word.name},\n\t{defin.grammar}"
                  f" {defin.body}{second} >< [{defin.case_tags}]\n")
        else:
            print(defin.source_word.name, result)


def check_sources_primitives():
    """

    :return:
    """
    c_type = Type.query.filter(Type.type == "C-Prim").first()
    words = Word.query.filter(Word.type_id == c_type.id).filter(~Word.origin.like("% | %")).all()
    _ = [print(word.__dict__) for word in words]


def check_sources_prim_d():
    """

    :return:
    """
    d_type = Type.query.filter(Type.type == "D-Prim").first()
    words = Word.query.filter(Word.type_id == d_type.id).all()
    _ = [print(word.get_sources_prim()) for word in words]


def check_complex_sources():
    """

    :return:
    """
    log.info("Start checking sources of Cpxes")
    cpx_type_ids = [t.id for t in Type.query.filter(Type.group == "Cpx").all()]
    words = Word.query.filter(Word.type_id.in_(cpx_type_ids)).all()
    for word in words:
        log.debug("Checking word: %s", word.name)
        trigger = 0
        sources = word.get_sources_cpx(as_str=True)
        for source in sources:
            if not Word.query.filter(Word.name == source).first():
                trigger = 1
                print(f"Word '{source}' is not in the Dictionary")
        if trigger:
            print(f"{word.id_old} |\t{word.name} |\t{word.origin} |\t{word.origin_x}")
    log.info("Finish checking sources of Cpxes")


def check_unintelligible_ccc():
    """

    :return:
    """
    log.info("Start checking unintelligible CCC")

    unintelligible_ccc = [
        syllable.name for syllable in
        Syllable.query.filter(Syllable.type == "UnintelligibleCCC").all()]
    ccc_filter = Word.name.like(any_([f"%{ccc}%" for ccc in unintelligible_ccc]))
    words = Word.by_event().filter(ccc_filter).all()
    _ = [print(word.name) for word in words]
    log.info("Finish checking unintelligible CCC")


def get_list_of_lw_with_wrong_linguistic_formula():
    """All LW should follow the formula (C)V(V).
    This function collect all LW that does not match it.
    """
    type_lw = [t.id for t in Type.query.filter(Type.type.in_(["LW", ])).all()]

    words = Word.by_event().filter(Word.type_id.in_(type_lw)).all()
    print(len(words))
    pattern = r"^[bcdfghjklmnprstvz]{0,1}[aoeiu]{1}[aoeiu]{0,1}$"

    for word in words:
        res = bool(re.match(pattern, word.name.lower()))

        if not res:
            print(f"{word.id_old} {word.name}, {res}")

    print(len([word for word in words if
               not bool(re.match(pattern, word.name.lower()))]))


if __name__ == "__main__":

    from loglan_db import app_lod
    with app_lod().app_context():
        pass
