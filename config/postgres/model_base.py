# -*- coding: utf-8 -*-

"""
Models of LOD database
"""

from __future__ import annotations
import re
from datetime import datetime
from typing import Set, List, Union, Optional
from sqlalchemy import exists, or_

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


class InitBase:
    """
    Init class for common methods
    """

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items() if not str(k).startswith("_")})

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


class DictionaryBase(InitBase):
    """Workaround for separating classes and making inheritance selections"""


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
    def attributes_all(cls) -> Set[str]:
        """
        :return:
        """
        return {key for key in cls.__mapper__.attrs.keys() if not key.startswith("_")}

    @classmethod
    def attributes_basic(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.attributes_all() - cls.relationships())

    @classmethod
    def attributes_extended(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.attributes_all() - cls.foreign_keys())

    @classmethod
    def relationships(cls) -> Set[str]:
        """
        :return:
        """
        return {key for key in cls.__mapper__.relationships.keys() if not key.startswith("_")}

    @classmethod
    def foreign_keys(cls) -> Set[str]:
        """
        :return:
        """
        return set(cls.attributes_all() - cls.relationships() - cls.non_foreign_keys())

    @classmethod
    def non_foreign_keys(cls) -> Set[str]:
        """
        :return:
        """
        return {column.name for column in cls.__table__.columns
                if not (column.foreign_keys or column.name.startswith("_"))}


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

    @classmethod
    def latest(cls):
        """
        :return: the latest (current) event
        """
        return cls.query.order_by(-cls.id).first()


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

    id = db.Column(db.Integer, primary_key=True)  # E.g. 4, 8
    type = db.Column(db.String(16), nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x = db.Column(db.String(16), nullable=False)  # E.g. Predicate, Predicate
    group = db.Column(db.String(16))  # E.g. Cpx, Prim
    parentable = db.Column(db.Boolean, nullable=False)  # E.g. True, False
    description = db.Column(db.String(255))  # E.g. Two-term Complex, ...


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

    APPROVED_CASE_TAGS = ["B", "C", "D", "F", "G", "J", "K", "N", "P", "S", "V", ]

    keys = db.relationship(Key.__name__, secondary=t_connect_keys,
                           backref="definitions", lazy='dynamic')

    def link_keys_from_list_of_str(
            self, source: List[str],
            language: str = None) -> List[Key]:
        """
        Linking a list of vernacular words with Definition
        Only new words will be linked, skipping those that were previously linked

        :param source: List of words on vernacular language
        :param language: Language of source words
        :return: List of linked Key objects
        """

        language = language if language else self.language

        new_keys = Key.query.filter(
            Key.word.in_(source),
            Key.language == language,
            ~exists().where(Key.id == self.keys.subquery().c.id),
        ).all()

        self.keys.extend(new_keys)
        return new_keys

    def link_key_from_str(self, word: str, language: str = None) -> Optional[Key]:
        """
        Linking vernacular word with Definition object
        Only new word will be linked, skipping this that was previously linked

        :param word: Word on vernacular language
        :param language: Words language
        :return: Linked Key object or None if it were already linked
        """
        language = language if language else self.language
        result = self.link_keys_from_list_of_str(source=[word, ], language=language)
        return result[0] if result else None

    def link_keys_from_list_of_obj(self, source: List[Key]) -> List[Key]:
        """
        Linking Key objects with Definition
        Only new Keys will be linked, skipping those that were previously linked

        :param source: List of Key objects from db
        :return: List of linked Key objects
        """
        new_keys = list(set(source) - set(self.keys))
        self.keys.extend(new_keys)
        return new_keys

    def link_key_from_obj(self, key: Key) -> Optional[Key]:
        """
        Linking Key object with Definition object
        It will be skipped if the Key has already been linked before
        :param key: Key objects from db
        :return: linked Key object or None if it were already linked
        """
        if key and not self.keys.filter(Key.id == key.id).count() > 0:
            self.keys.append(key)
            return key
        return None

    def link_keys_from_definition_body(
            self, language: str = None,
            pattern: str = None) -> List[Key]:
        """
        Extract and link keys from Definition's body
        :param language: Language of Definition's keys
        :param pattern: Regex pattern for extracting keys from the Definition's body
        :return: List of linked Key objects
        """
        language = language if language else self.language
        pattern = r"(?<=\«)(.+?)(?=\»)" if not pattern else pattern
        keys = re.findall(pattern, self.body)
        return self.link_keys_from_list_of_str(source=keys, language=language)

    def link_keys(
            self, source: Union[List[Key], List[str], Key, str, None] = None,
            language: str = None, pattern: str = None) -> Union[Key, List[Key]]:
        """
        Universal method for linking all available types of key sources with Definition

        :param source: Could be a str, Key, List of Keys or str, or None
        If no source is provided, keys will be extracted from the Definition's body
        If source is a string or a list of strings, the language of the keys must be specified
        TypeError will be raised if the source contains inappropriate data
        :param language: Language of Definition's keys
        :param pattern: Regex pattern for extracting keys from the Definition's body
        :return: None, Key, or List of Keys
        """

        language = language if language else self.language

        if not source:
            return self.link_keys_from_definition_body(language=language, pattern=pattern)

        if isinstance(source, str):
            return self.link_key_from_str(word=source, language=language)

        if isinstance(source, Key):
            return self.link_key_from_obj(key=source)

        if isinstance(source, list):

            if all(isinstance(item, Key) for item in source):
                return self.link_keys_from_list_of_obj(source=source)

            if all(isinstance(item, str) for item in source):
                return self.link_keys_from_list_of_str(source=source, language=language)

        raise TypeError("Source for keys should have a string, "
                        "Key or list of strings or Keys type. "
                        "You input %s" % type(source))


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

    def add_children(self, children: List[Word]):
        """
        Add derivatives for the source word
        Get words from Used In and add relationship in database
        :param children: List of Word objects
        :return: None
        """
        new_children = list(set(children) - set(self.__derivatives))
        self.__derivatives.extend(new_children) if new_children else None

    def add_author(self, author: Author) -> str:
        """
        Connect Author object with Word object
        :param author: Author object
        :return:
        """
        if not self.authors.filter(Author.abbreviation == author.abbreviation).count() > 0:
            self.authors.append(author)
        return author.abbreviation

    def add_authors(self, authors: List[Author]):
        """
        Connect Author objects with Word object
        :param authors: List of Author object
        :return:
        """
        new_authors = list(set(authors) - set(self.authors))
        self.authors.extend(new_authors) if new_authors else None

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

    def get_sources_prim(self, prim_type: str):
        """
        :param prim_type:
        :return:
        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not self.type.group == "Prim":
            return []

        prim_type = self.type.type[:1]

        if prim_type == "C":
            return self._get_sources_c_prim()

        if prim_type == "D":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        if prim_type == "I":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        if prim_type == "L":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        if prim_type == "N":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        if prim_type == "O":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        if prim_type == "S":  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        return list()

    def _get_sources_c_prim(self) -> List[WordSource]:
        """
        :return:
        """
        if self.type.type != "C-Prim":
            return []

        pattern_source = r"\d+\/\d+\w"
        sources = str(self.origin).split(" | ")
        word_sources = []

        for source in sources:
            compatibility = re.search(pattern_source, source)[0]
            c_l = compatibility[:-1].split("/")
            transcription = (re.search(rf"(?!{pattern_source}) .+", source)[0]).strip()
            word_source = WordSource(**{
                "coincidence": int(c_l[0]),
                "length": int(c_l[1]),
                "language": compatibility[-1:],
                "transcription": transcription, })
            word_sources.append(word_source)

        return word_sources

    def get_sources_cpx(self, as_objects: bool = False) -> List[Union[str, Word]]:
        """
        Get self.origin and extract source words accordingly
        :param as_objects: Boolean - return Word objects if true else as simple str
        :return: List of words from which the self.name was created

        Example: 'foldjacea' > ['forli', 'djano', 'cenja']
        """

        # these prims have switched djifoas like 'flo' for 'folma'
        switch_prims = [
            'canli', 'farfu', 'folma', 'forli', 'kutla', 'marka',
            'mordu', 'sanca', 'sordi', 'suksi', 'surna']

        if not self.type.group == "Cpx":
            return []

        sources = self.origin.replace("(", "").replace(")", "").replace("/", "")
        sources = str(sources).split("+")
        sources = [s for s in sources if s not in ["y", "r", "n"]]
        sources = [
            s if not (s.endswith("r") or s.endswith("h")) else s[:-1]
            for s in sources if s not in ["y", "r"]]
        return sources if not as_objects else Word.query.filter(Word.name.in_(sources)).all()

    @classmethod
    def get_items_by_event(cls, event_id: int = None):
        """
        Filtered request by specified event_id
        :param event_id: Latest if None
        :return: Request
        """
        if not event_id:
            event_id = Event.latest().id

        return cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None))) \
            .order_by(cls.name)


class WordSource(InitBase):
    """
    Word Source from Word.origin for Prims
    """

    LANGUAGES = {
        "E": "English",
        "C": "Chinese",
        "H": "Hindi",
        "R": "Russian",
        "S": "Spanish",
        "F": "French",
        "J": "Japanese",
        "G": "German", }

    coincidence: int = None
    length: int = None
    language: str = None
    transcription: str = None

    @property
    def as_string(self):  # For example, '3/5R mesto'
        """
        :return:
        """
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"


class WordSpell(DictionaryBase, ConvertWordSpell):
    """WordSpell model"""
    __tablename__ = t_name_word_spells
