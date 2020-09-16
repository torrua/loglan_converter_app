"""
Module for check database data
"""
import re
from config.postgres.model_base import Word, Definition


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
    words = Word.get_all()
    for word in words:
        if word.type.type == "C-Prim" and " | " not in word.origin:
            print(word.__dict__)


def check_sources_prim_d():
    words = Word.get_all()
    for word in words:
        if word.type.type == "D-Prim":
            print(word.get_sources_prim("D"))


def check_sources_prim(prim_type: str):
    words = Word.get_all()
    for word in words:
        if word.type.type == f"{prim_type}-Prim":
            print(word.get_sources_prim(prim_type))


def check_complex_sources():
    words = Word.get_all()
    for word in words:
        trigger = 0
        if word.type.group == "Cpx":
            sources = word.get_sources_cpx()
            for s in sources:
                w = Word.query.filter(Word.name == s).first()
                if not w:
                    trigger = 1
                    print(f"Word '{s}' is not in the Dictionary")
        if trigger:
            print(f"{word.id_old} |\t{word.name} |\t{word.origin} |\t{word.origin_x}")


def check_unintelligible_ccc():
    unintelligible_ccc = [
        "cdz", "cvl", "ndj", "ndz",
        "dcm", "dct", "dts", "pdz",
        "gts", "gzb", "svl", "jdj",
        "jtc", "jts", "jvr", "tvl",
        "kdz", "vts", "mzb", ]

    for word in Word.get_all():
        if any(x in word.name for x in unintelligible_ccc):
            print(word.__dict__)


if __name__ == "__main__":
    from config.postgres import CLIConfig, create_app_lod

    with create_app_lod(CLIConfig).app_context():
        pass
