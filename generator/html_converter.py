# -*- coding: utf-8 -*-
"""
HTML Generator
"""

import time
from datetime import datetime, timedelta
from itertools import groupby
from sqlalchemy import or_

from jinja2 import Environment, PackageLoader

from config import create_app, log, DEFAULT_LANGUAGE, DEFAULT_STYLE
from config.postgres import CLIConfig
from config.postgres.model_base import Key
from config.postgres.model_export import ExportSetting, ExportEvent
from config.postgres.model_html import HTMLExportWord, HTMLExportDefinition


# TODO Add normal template
# TODO Add other languages support


def prepare_dictionary_l(style: str = DEFAULT_STYLE, lex_event: int = None):
    """

    :param style:
    :param lex_event:
    :return:
    """

    if lex_event is None:
        lex_event = ExportEvent.query.order_by(-ExportEvent.id).first().id

    all_words = HTMLExportWord.query \
        .filter(HTMLExportWord.event_start_id <= lex_event) \
        .filter(or_(HTMLExportWord.event_end_id > lex_event, HTMLExportWord.event_end_id.is_(None)))\
        .order_by(HTMLExportWord.name).all()  # [1350:1400]

    grouped_words = groupby(all_words, lambda ent: ent.name)
    group_words = {k: list(g) for k, g in grouped_words}

    grouped_letters = groupby(group_words, lambda ent: ent[0].upper())
    names_grouped_by_letter = {k: list(g) for k, g in grouped_letters}

    dictionary = {}
    for letter, names in names_grouped_by_letter.items():
        dictionary[letter] = [{
            "name": group_words[name][0].name,
            "meanings": [w.meaning(style=style) for w in group_words[name]]} for name in names]

    return dictionary


def prepare_dictionary_e(style: str = DEFAULT_STYLE, key_language: str = DEFAULT_LANGUAGE, lex_event: int = None):
    """

    :param style:
    :param key_language:
    :param lex_event:
    :return:
    """
    def check_events(d: HTMLExportDefinition, event: int):
        if d.source_word.event_start_id > event:
            return False
        if d.source_word.event_end_id is None:
            return True
        if d.source_word.event_end_id > event:
            return True
        return False

    if lex_event is None:
        lex_event = ExportEvent.query.order_by(-ExportEvent.id).first().id

    all_keys = Key.query.order_by(Key.word).filter(Key.language == key_language).all()  # [1600:1700]
    all_keys_words = [key.word for key in all_keys]

    grouped_keys = groupby(all_keys, lambda ent: ent.word)

    group_keys = {k: [
        HTMLExportDefinition.export_for_english(d, word=k, style=style)
        for d in list(g)[0].definitions if check_events(d, lex_event)]
        for k, g in grouped_keys}

    grouped_letters = groupby(all_keys_words, lambda ent: ent[0].upper())
    key_names_grouped_by_letter = {k: sorted(list(g)) for k, g in grouped_letters}

    return {
        letter: {name: group_keys[name] for name in names}
        for letter, names in key_names_grouped_by_letter.items()}


def prepare_technical_info(lex_event: int = None):
    generation_date = datetime.now().strftime("%d.%m.%Y")
    db_release = ExportSetting.query.order_by(-ExportSetting.id).first().db_release

    if lex_event is None:
        lex_event = ExportEvent.query.order_by(-ExportEvent.id).first().id

    event = ExportEvent.query.filter(ExportEvent.id == lex_event).first().annotation
    return {
        "Generated": generation_date,
        "Database": db_release,
        "LexEvent": event, }


def generate_dictionary_file(entities_language: str = "loglan", style: str = DEFAULT_STYLE, lex_event: int = None):
    """
    :param entities_language: [ loglan, english ]
    :param style: [ normal, ultra ]
    :param lex_event:
    """

    env = Environment(loader=PackageLoader('generator', f'templates/{entities_language}'))

    if entities_language == "loglan":
        data = prepare_dictionary_l(style=style, lex_event=lex_event)
    else:
        data = prepare_dictionary_e(style=style, lex_event=lex_event)

    template = env.get_template(f'words_{style}.html')
    tech = prepare_technical_info(lex_event=lex_event)
    t = template.render(dictionary=data, technical=tech)
    name = "L-to-E" if entities_language == "loglan" else "E-to-L"
    file = f"{name}-{tech['Database']}-{datetime.now().strftime('%y%m%d%H%M')}.html"
    text_file = open(file, "w", encoding="utf-8")
    text_file.write(t)
    text_file.close()


if __name__ == "__main__":

    with create_app(CLIConfig).app_context():
        log.info("START DICTIONARY HTML CREATION")
        start_time = time.monotonic()
        generate_dictionary_file(entities_language="english")
        generate_dictionary_file(entities_language="loglan")
        log.info("ELAPSED TIME IN MINUTES: %s\n", timedelta(minutes=time.monotonic() - start_time))
