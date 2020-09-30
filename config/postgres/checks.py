# -*- coding: utf-8 -*-
"""
Module for check database data
"""

import re

from sqlalchemy import any_

from config import log
from config.postgres.model_base import Word, Definition, Type, Syllable


def check_tag_match(extended_result: bool = False):
    """
    Determine the discrepancy between the declared tags and those actually specified in the Definition
    :param extended_result: If True, returns an expanded dataset instead of a boolean
    :return: Boolean or tuple, depending on the extended_result variable
    """
    definitions = Definition.query.filter(Definition.case_tags != "").all()
    for df in definitions:

        pattern_case_tags = f"[{''.join(Definition.APPROVED_CASE_TAGS)}]"
        list_tags = re.findall(pattern_case_tags, df.case_tags)
        list_body = [tag for tag in re.findall(r'\w+', df.body) if tag in Definition.APPROVED_CASE_TAGS]

        result = list_tags == list_body

        if result:
            continue

        if extended_result:
            print(df.source_word.name, result, list_tags, list_body)
        else:
            print(df.source_word.name, result)


def check_sources_primitives():
    c_type = Type.query.filter(Type.type == "C-Prim").first()
    words = Word.query.filter(Word.type_id == c_type.id).filter(~Word.origin.like("% | %")).all()
    [print(word.__dict__) for word in words]


def check_sources_prim_d():
    d_type = Type.query.filter(Type.type == "D-Prim").first()
    words = Word.query.filter(Word.type_id == d_type.id).all()
    [print(word.get_sources_prim()) for word in words]


def check_complex_sources():
    log.info("Start checking sources of Cpxes")
    cpx_type_ids = [t.id for t in Type.query.filter(Type.group == "Cpx").all()]
    words = Word.query.filter(Word.type_id.in_(cpx_type_ids)).all()
    for word in words:
        log.debug("Checking word: %s", word.name)
        trigger = 0
        sources = word.get_sources_cpx(as_str=True)
        for s in sources:
            if not Word.query.filter(Word.name == s).first():
                trigger = 1
                print(f"Word '{s}' is not in the Dictionary")
        if trigger:
            print(f"{word.id_old} |\t{word.name} |\t{word.origin} |\t{word.origin_x}")
    log.info("Finish checking sources of Cpxes")


def check_unintelligible_ccc():
    log.info("Start checking unintelligible CCC")

    unintelligible_ccc = [s.name for s in Syllable.query.filter(Syllable.type == "UnintelligibleCCC").all()]
    ccc_filter = Word.name.like(any_([f"%{ccc}%" for ccc in unintelligible_ccc]))
    words = Word.by_event().filter(ccc_filter).all()
    [print(word.name) for word in words]
    log.info("Finish checking unintelligible CCC")


if __name__ == "__main__":
    from config.postgres import CLIConfig, app_lod
    with app_lod(CLIConfig).app_context():
        pass
