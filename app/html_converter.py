# -*- coding: utf-8 -*-
"""
HTML Generator
"""

import time
from datetime import datetime, timedelta
from itertools import groupby

from jinja2 import Environment, PackageLoader

from config import create_app, log, DEFAULT_LANGUAGE, DEFAULT_STYLE
from config.postgres import CLIConfig
from config.postgres.model_base import Key
from config.postgres.model_export import ExportSetting
from config.postgres.model_html import HTMLExportWord, HTMLExportDefinition


def prepare_dictionary_data_l(style: str = DEFAULT_STYLE, lex_event: str = None):

    all_words = HTMLExportWord.query.\
        filter(HTMLExportWord.event_end_id.is_(lex_event)).\
        order_by(HTMLExportWord.name).all()  # [1350:1400]
    grouped_words = groupby(all_words, lambda ent: ent.name)

    group_words = {k: list(g) for k, g in grouped_words}
    grouped_letters = groupby(group_words, lambda ent: ent[0].upper())
    names_grouped_by_letter = {k: list(g) for k, g in grouped_letters}
    dictionary = {}
    for letter, names in names_grouped_by_letter.items():
        dictionary[letter] = [{
            "name": group_words[name][0].name,
            "meanings": [w.meaning(style=style) for w in group_words[name]]} for name in names]

    generation_date = datetime.now().strftime("%d.%m.%Y")
    db_release = ExportSetting.query.order_by(-ExportSetting.id).first().db_release

    return {
        "dictionary": dictionary,
        "technical": {
            "generation_date": generation_date,
            "db_release": db_release,
            "lex_event": "latest", }}


def prepare_dictionary_data_e(style: str = DEFAULT_STYLE, key_language: str = DEFAULT_LANGUAGE):
    all_keys = Key.query.order_by(Key.word).filter(Key.language == key_language).all()  # [1600:1700]
    all_keys_words = [key.word for key in all_keys]

    grouped_keys = groupby(all_keys, lambda ent: ent.word)
    group_keys = {k: [
        HTMLExportDefinition.export_for_english(d, word=k, style=style)
        for d in list(g)[0].definitions
        if d.source_word.event_end_id is None]
        for k, g in grouped_keys}

    grouped_letters = groupby(all_keys_words, lambda ent: ent[0].upper())
    key_names_grouped_by_letter = {k: sorted(list(g)) for k, g in grouped_letters}

    dictionary = {
        letter: {name: group_keys[name] for name in names}
        for letter, names in key_names_grouped_by_letter.items()}

    generation_date = datetime.now().strftime("%d.%m.%Y")
    db_release = ExportSetting.query.order_by(-ExportSetting.id).first().db_release
    return {
        "dictionary": dictionary,
        "technical": {
            "generation_date": generation_date,
            "db_release": db_release,
            "lex_event": "latest", }}


def generate_dictionary_file(entities_language: str = "logla", style: str = DEFAULT_STYLE):
    """
    :param entities_language: [ logla, gleci ]
    :param style: [ normal, ultra ]
    :return:
    """

    env = Environment(loader=PackageLoader('app', f'templates/{entities_language}'))

    if entities_language == "gleci":
        data = prepare_dictionary_data_e(style)
    else:
        data = prepare_dictionary_data_l(style)

    template = env.get_template(f'words_{style}.html')
    t = template.render(data=data)
    file = f"{entities_language}_({datetime.now().strftime('%y%m%d%H%M')})_{style}.html"
    text_file = open(file, "w", encoding="utf-8")
    text_file.write(t)
    text_file.close()


if __name__ == "__main__":
    with create_app(CLIConfig).app_context():
        log.info("START DICTIONARY HTML CREATION")
        start_time = time.monotonic()
        generate_dictionary_file()
        log.info("ELAPSED TIME IN MINUTES: %s\n", timedelta(minutes=time.monotonic() - start_time))
