"""
This module contains default classes for LOD data conversion
"""
# pylint: disable=too-many-ancestors

from loglan_db.model import Key as SourceKey, WordSource as SourceWordSource

from loglan_db.model_export import ExportAuthor, ExportEvent, \
    ExportSetting, ExportSyllable, ExportType, \
    ExportDefinition, ExportWord, ExportWordSpell

from config.postgres.model_convert import ConvertAuthor, ConvertEvent, \
    ConvertKey, ConvertSetting, ConvertSyllable, ConvertType, \
    ConvertDefinition, ConvertWord, ConvertWordSpell


class DictionaryBase:  # pylint: disable=too-few-public-methods
    """Workaround for separating classes and making inheritance selections"""


class Author(DictionaryBase, ConvertAuthor, ExportAuthor):
    """Default Author class for conversion"""


class Event(DictionaryBase, ConvertEvent, ExportEvent):
    """Default Event class for conversion"""


class Key(DictionaryBase, SourceKey, ConvertKey):
    """Default Key class for conversion"""


class Setting(DictionaryBase, ConvertSetting, ExportSetting):
    """Default Setting class for conversion"""


class Syllable(DictionaryBase, ConvertSyllable, ExportSyllable):
    """Default Syllable class for conversion"""


class Type(DictionaryBase, ConvertType, ExportType):
    """Default Type class for conversion"""


class Definition(DictionaryBase, ConvertDefinition, ExportDefinition):
    """Default Definition class for conversion"""


class Word(DictionaryBase, ConvertWord, ExportWord):
    """Default Word class for conversion"""


class WordSpell(DictionaryBase, ConvertWordSpell, ExportWordSpell):
    """Default WordSpell class for conversion"""


class WordSource(SourceWordSource):
    """Default WordSource class for conversion"""


all_models_pg = sorted(
    DictionaryBase.__subclasses__(),
    key=lambda model: model.__index_sort_import__)

export_models_pg = sorted(
    [model for model in all_models_pg if model.__load_to_file__],
    key=lambda model: model.__index_sort_import__)
