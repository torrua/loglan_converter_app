# -*- coding: utf-8 -*-
# pylint: disable=R0903, E1101, C0103

"""
Models of LOD database with extensions for converting
"""

from config.postgres import db
from config.postgres.model_convert import ConvertAuthor, ConvertEvent, ConvertKey, ConvertSetting, ConvertSyllable, \
    ConvertType, ConvertDefinition, ConvertWord, ConvertWordSpell
from config.postgres.model_base import Author, Event, Key, Setting, Syllable, Type, Definition, Word, WordSpell

db.metadata.clear()


class DictionaryBase:
    """
    Base class for common methods
    """

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def export(self):
        """
        Export record data from DB
        Should be redefine in model's class
        :return:
        """

    def import_(self):
        """
        Import txt data to DB
        Should be redefine in model's class
        :return:
        """


class ComplexAuthor(Author, DictionaryBase, ConvertAuthor):
    pass


class ComplexEvent(Event, DictionaryBase, ConvertEvent):
    pass


class ComplexKey(Key, DictionaryBase, ConvertKey):
    pass


class ComplexSetting(Setting, DictionaryBase, ConvertSetting):
    pass


class ComplexSyllable(Syllable, DictionaryBase, ConvertSyllable):
    pass


class ComplexType(Type, DictionaryBase, ConvertType):
    pass


class ComplexDefinition(Definition, DictionaryBase, ConvertDefinition):
    pass


class ComplexWord(Word, DictionaryBase, ConvertWord):
    pass


class ComplexWordSpell(WordSpell, DictionaryBase, ConvertWordSpell):
    pass


if __name__ == "__main__":
    db.create_all()
