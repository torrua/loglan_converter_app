from config.sqlite import run_with_context, db
from config.sqlite.model import Key, Meaning
from reverso_api.context import ReversoContextAPI
import operator
from typing import List
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from translator import SOURCE_LANGUAGE, TARGET_LANGUAGE

"""
@run_with_context
def translate_keys():
    keys = Key.get_all()[5400:5450]
    for key in keys:
        print(key.word)
        for kt in merged_translations(key.word):
            print(kt)
        print()
"""
# TODO optimize and add more structure


def get_translations(word: str, source_lang: str = SOURCE_LANGUAGE, target_lang: str = TARGET_LANGUAGE):
    """
    Get translations of desired word
    :param word: str with desired word
    :param source_lang:
    :param target_lang:
    :return: list of translations
    """
    api = ReversoContextAPI(source_text=word, source_lang=source_lang, target_lang=target_lang)
    translations = [t for t in api.get_translations()]
    return reversed(sorted(translations, key=operator.attrgetter('frequency')))


def merged_translations(word: str) -> List[dict]:
    """
    Merge normalized words
    :param word:
    :return: List of dicts with normalized merged words
    """
    words = [w for w in get_translations(word)]

    # clean and normalize results
    translations_for_merging = []
    for w in words:
        item = {
            k: v if k != 'translation' else morph.parse(v)[0].normal_form
            for k, v in dict(w._asdict()).items()
            if k != "inflected_forms"
        }
        if not item["translation"].isascii():
            translations_for_merging.append(item)

    all_vernacular_words = set([w["translation"] for w in translations_for_merging])
    unique_vernacular_words = [
        {"translation": w, "frequency": 0, "part_of_speech": list()}
        for w in all_vernacular_words]

    # merge items data
    for item in translations_for_merging:
        for jtem in unique_vernacular_words:

            if item["translation"] != jtem["translation"]:
                continue

            jtem["frequency"] += item["frequency"]

            if item["part_of_speech"] not in [*jtem["part_of_speech"], "", None]:
                jtem["part_of_speech"].append(item["part_of_speech"])

    return sorted(unique_vernacular_words, key=operator.itemgetter('frequency'), reverse=True)


@run_with_context
def save_keys_to_sdb(keys: List[dict]):
    print(keys)
    for key in keys:
        print(key["word"])
        Key(**key).save()


@run_with_context
def add_meanings_to_keys():

    for key in Key.query.all():
        print(key.word)
        meanings = [(Meaning(**m, language="ru")) for m in merged_translations(key.word)]
        key.add_meanings(meanings)
    db.session.commit()


if __name__ == "__main__":
    # keys = get_p_keys()
    # print(keys)
    add_meanings_to_keys()
