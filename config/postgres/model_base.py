# -*- coding: utf-8 -*-
# pylint: disable=R0903, E1101, C0103

"""
Models of LOD database
"""

from __future__ import annotations

from datetime import datetime
from typing import Set, List

from config.postgres import db
from config.postgres.model_convert import ConvertAuthor, ConvertEvent, \
    ConvertKey, ConvertSetting, ConvertSyllable, ConvertType, \
    ConvertDefinition, ConvertWord, ConvertWordSpell

t_name_authors = "authors"
t_name_events = "events"
t_name_keys = "keys"
t_name_settings = "settings"
t_name_syllables = "syllables"
t_name_types = "types"
t_name_words = "words"
t_name_definitions = "definitions"
t_name_x_words = "x_words"
t_name_word_spells = "word_spells"

db.metadata.clear()

t_connect_authors = db.Table(
    'connect_authors', db.metadata,
    db.Column('AID', db.ForeignKey(f'{t_name_authors}.id'), primary_key=True),
    db.Column('WID', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
t_connect_words = db.Table(
    'connect_words', db.metadata,
    db.Column('parent_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True),
    db.Column('child_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
t_connect_keys = db.Table(
    'connect_keys', db.metadata,
    db.Column('KID', db.ForeignKey(f'{t_name_keys}.id'), primary_key=True),
    db.Column('DID', db.ForeignKey(f'{t_name_definitions}.id'), primary_key=True), )


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


class DBBase:
    """Common methods and attributes for basic models"""
    created = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)
    updated = db.Column(db.TIMESTAMP, onupdate=db.func.now())
    __table__ = None
    __mapper__ = None

    def save(self) -> None:
        """
        Add record to DB
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, data) -> None:
        """
        Update record in DB
        :param data:
        :return:
        """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self) -> None:
        """
        Delete record from DB
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List:
        """
        Get all model objects from DB
        :return:
        """
        return cls.query.all()

    @classmethod
    def non_foreign_keys(cls) -> Set[str]:
        """
        :return:
        """
        return {column.name for column in cls.__table__.columns
                if not (column.foreign_keys or column.name.startswith("_"))}

    @classmethod
    def relationships(cls) -> Set[str]:
        """
        :return:
        """
        return {key for key in cls.__mapper__.relationships.keys() if not key.startswith("_")}

    @classmethod
    def all_attributes(cls) -> Set[str]:
        """
        :return:
        """
        return {key for key in cls.__mapper__.attrs.keys() if not key.startswith("_")}

    @classmethod
    def foreign_keys(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.all_attributes() - cls.relationships() - cls.non_foreign_keys())

    @classmethod
    def attributes_basic(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.all_attributes() - cls.relationships())

    @classmethod
    def attributes_extended(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.all_attributes() - cls.foreign_keys())


class Author(db.Model, DictionaryBase, DBBase, ConvertAuthor):
    """
    Author model
    """
    __tablename__ = t_name_authors

    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(64), unique=True, nullable=False)
    full_name = db.Column(db.String(64))
    notes = db.Column(db.String(128))


class Event(db.Model, DictionaryBase, DBBase, ConvertEvent):
    """
    Event model
    """
    __tablename__ = t_name_events

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    annotation = db.Column(db.String(16), nullable=False)
    suffix = db.Column(db.String(16), nullable=False)


class Key(db.Model, DictionaryBase, DBBase, ConvertKey):
    """
    Key model
    """
    __tablename__ = t_name_keys

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(16))


class Setting(db.Model, DictionaryBase, DBBase, ConvertSetting):
    """
    Setting model
    """
    __tablename__ = t_name_settings

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    db_version = db.Column(db.Integer, nullable=False)
    last_word_id = db.Column(db.Integer, nullable=False)
    db_release = db.Column(db.String(16), nullable=False)


class Syllable(db.Model, DictionaryBase, DBBase, ConvertSyllable):
    """
    Syllable model
    """
    __tablename__ = t_name_syllables

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    allowed = db.Column(db.Boolean)


class Type(db.Model, DictionaryBase, DBBase, ConvertType):
    """
    Type model
    """
    __tablename__ = t_name_types

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    type_x = db.Column(db.String(16), nullable=False)
    group = db.Column(db.String(16))
    parentable = db.Column(db.Boolean, nullable=False)


class Definition(db.Model, DictionaryBase, DBBase, ConvertDefinition):
    """
    Definition model
    """
    __tablename__ = t_name_definitions

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey(f'{t_name_words}.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    usage = db.Column(db.String(64))
    grammar_code = db.Column(db.String(8))
    slots = db.Column(db.Integer)
    case_tags = db.Column(db.String(16))
    body = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(16))
    notes = db.Column(db.String(255))

    keys = db.relationship(Key.__name__, secondary=t_connect_keys,
                           backref="definitions", lazy='dynamic')

    def add_key(self, key: Key) -> bool:
        """
        Connect Key object with Definition object
        :param key: Key object
        :return:
        """

        if key and not self.keys.filter(Key.word == key.word).count() > 0:
            self.keys.append(key)
            return True
        return False


class Word(db.Model, DictionaryBase, DBBase, ConvertWord):
    """
    Word model
    """
    __tablename__ = t_name_words

    id = db.Column(db.Integer, primary_key=True)
    id_old = db.Column(db.Integer, nullable=False)  # Compatibility with the previous database
    name = db.Column(db.String(64), nullable=False)
    origin = db.Column(db.String(128))
    origin_x = db.Column(db.String(64))

    type_id = db.Column("type", db.ForeignKey(f'{t_name_types}.id'), nullable=False)
    type = db.relationship(Type.__name__, backref="words")

    event_start_id = db.Column("event_start", db.ForeignKey(f'{t_name_events}.id'), nullable=False)
    event_start = db.relationship(
        "Event", foreign_keys=[event_start_id], backref="appeared_words")

    event_end_id = db.Column("event_end", db.ForeignKey(f'{t_name_events}.id'))
    event_end = db.relationship(
        "Event", foreign_keys=[event_end_id], backref="deprecated_words")

    match = db.Column(db.String(8))
    rank = db.Column(db.String(8))
    year = db.Column(db.Date)
    notes = db.Column(db.JSON)
    TID_old = db.Column(db.Integer)  # references

    authors = db.relationship(Author.__name__,
                              secondary=t_connect_authors,
                              backref="contribution",
                              lazy='dynamic')

    definitions = db.relationship("Definition", backref="source_word", lazy='dynamic')

    # word's derivatives
    __derivatives = db.relationship(
        'Word', secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=db.backref('parents', lazy='dynamic'),
        lazy='dynamic')

    def __is_parented(self, child: Word) -> bool:
        """
        Check, if this word is already added as a parent for this 'child'
        :param child: Word object
        :return: bool
        """
        return self.__derivatives.filter(t_connect_words.c.child_id == child.id).count() > 0

    def add_child(self, child: Word) -> str:
        """
        Add derivative for the source word
        Get words from Used In and add relationship in database
        :param child: Word object
        :return: None
        """
        if not self.__is_parented(child):
            self.__derivatives.append(child)
        return child.name

    def add_author(self, author: Author) -> str:
        """
        Connect Author object with Word object
        :param author: Author object
        :return:
        """
        if not self.authors.filter(Author.abbreviation == author.abbreviation).count() > 0:
            self.authors.append(author)
        return author.abbreviation

    def get_definitions(self) -> List[Definition]:
        """
        Get all definitions of the word
        :return: List of Definition objects ordered by Definition.position
        """
        return Definition.query.filter(Definition.id == self.id)\
            .order_by(Definition.position.asc()).all()

    def get_parents(self) -> List[Word]:
        """
        Get all parents of the Complex predicates, Little words or Affixes
        :return: List of Word objects
        """
        return self.parents.all()  # if self.type in self.__parentable else []

    def get_derivatives(self,
                        word_type: str = None,
                        word_type_x: str = None,
                        word_group: str = None) -> List[Word]:
        """
        Get all derivatives of the word, depending on its parameters
        :param word_type:
        :param word_type_x:
        :param word_group:
        :return:
        """
        result = self.__derivatives.filter(self.id == t_connect_words.c.parent_id)

        if word_type or word_type_x or word_group:
            result = result.join(Type)

        if word_type:
            result = result.filter(Type.type == word_type)
        if word_type_x:
            result = result.filter(Type.type_x == word_type_x)
        if word_group:
            result = result.filter(Type.group == word_group)

        return result.order_by(Word.name.asc()).all()

    def get_cpx(self) -> List[Word]:
        """
        Get all the complexes that exist for this word
        Only primitives have affixes
        :return: list of Word objects
        """
        return self.get_derivatives(word_group="Cpx")

    def get_afx(self) -> List[Word]:
        """
        Get all the affixes that exist for this word
        Only primitives have affixes
        :return: list of Word objects
        """
        return self.get_derivatives(word_type="Afx")

    @property
    def complexes(self) -> List[Word]:
        """
        Get list of word's complexes if exist
        :return:
        """
        return self.get_cpx()

    @property
    def affixes(self) -> List[Word]:
        """
        Get list of word's affixes if exist
        :return:
        """
        return self.get_afx()


class WordSpell(DictionaryBase, ConvertWordSpell):
    """WordSpell model"""
    __tablename__ = t_name_word_spells
