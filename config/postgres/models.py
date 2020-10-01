from config.postgres.model_base import BaseAuthor, BaseEvent, \
    BaseKey, BaseSetting, BaseSyllable, BaseType, \
    BaseDefinition, BaseWord, BaseWordSpell, BaseWordSource

from config.postgres.model_convert import ConvertAuthor, ConvertEvent, \
    ConvertKey, ConvertSetting, ConvertSyllable, ConvertType, \
    ConvertDefinition, ConvertWord, ConvertWordSpell


class DictionaryBase:
    """Workaround for separating classes and making inheritance selections"""


class Author(DictionaryBase, BaseAuthor, ConvertAuthor):
    __mapper_args__ = {
        'polymorphic_identity': "authors",
    }


class Event(DictionaryBase, BaseEvent, ConvertEvent):
    pass


class Key(DictionaryBase, BaseKey, ConvertKey):
    pass


class Setting(DictionaryBase, BaseSetting, ConvertSetting):
    pass


class Syllable(DictionaryBase, BaseSyllable, ConvertSyllable):
    pass


class Type(DictionaryBase, BaseType, ConvertType):
    pass


class Definition(DictionaryBase, BaseDefinition, ConvertDefinition):
    pass


class Word(DictionaryBase, BaseWord, ConvertWord):
    pass


class WordSpell(DictionaryBase, BaseWordSpell, ConvertWordSpell):
    pass


class WordSource(BaseWordSource):
    pass


all_models_pg = sorted(
    [model for model in DictionaryBase.__subclasses__()],
    key=lambda model: model.__index_sort_import__)