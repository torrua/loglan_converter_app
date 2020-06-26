from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, UnicodeText
from config.access import Base
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class BaseFunctions:
    """
    Base class for common methods
    """
    __tablename__ = None

    @classmethod
    @declared_attr
    def import_file_name(cls):
        return f"{cls.__tablename__}.txt"

    @classmethod
    @declared_attr
    def export_file_name(cls):
        return f"AC_{datetime.now().strftime('%y%m%d%H%M')}_{cls.__tablename__}.txt"

    def __init__(self, *initial_data, **kwargs):
        """Constructor"""
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def export(self):
        pass


class AccessAuthor(Base, BaseFunctions):
    """
    Author model
    """
    __tablename__ = "Author"

    sort_name = "Author"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(64), unique=True, nullable=False)
    full_name = Column(String(255))
    notes = Column(String(255))


class AccessEvent(Base, BaseFunctions):
    """
    Event model
    """
    __tablename__ = "LexEvent"
    sort_name = "Event"

    id = Column("EVT", Integer, primary_key=True)
    name = Column("Event", Text, nullable=False)
    date = Column("When", Text, nullable=False)
    definition = Column("WhyWhat", Text, nullable=False)
    annotation = Column("DictionaryAnnotation", Text)
    suffix = Column("FilenameSuffix", Text)


class AccessSetting(Base, BaseFunctions):
    """
    Setting model
    """
    __tablename__ = "Settings"
    sort_name = "Settings"

    date = Column("DateModified", DateTime,  primary_key=True)
    db_version = Column("DBVersion", Integer, nullable=False)
    last_word_id = Column("LastWID", Integer, nullable=False)


class AccessSyllable(Base, BaseFunctions):
    """
    Syllable model
    """
    __tablename__ = "Syllable"
    sort_name = "Syllable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("characters", Text, primary_key=True)
    type = Column(Text, nullable=False)
    allowed = Column(Boolean)


class AccessType(Base, BaseFunctions):
    """
    Type model
    """
    __tablename__ = "Type"
    sort_name = "Type"

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    type_x = Column(String(255), nullable=False)
    group = Column(String(255))
    parentable = Column(Boolean, nullable=False)


class AccessDefinition(Base, BaseFunctions):
    __tablename__ = 'WordDefinition'
    sort_name = "Definition"

    word_id = Column("WID", Integer, primary_key=True)
    position = Column("I", Integer, primary_key=True)
    usage = Column("Usage", String(255))
    grammar = Column("Grammar", String(255))
    body = Column("Definition", UnicodeText, nullable=False)
    main = Column("Main", String(255))
    case_tags = Column("Tags", String(255))


class AccessWord(Base, BaseFunctions):
    """
    Word model
    """
    __tablename__ = "Words"
    sort_name = "Word"

    word_id = Column("WID", Integer, nullable=False, primary_key=True)
    type = Column("Type", String, nullable=False)
    type_x = Column("XType", String, nullable=False)
    affixes = Column("Affixes", String)
    match = Column("Match", String)
    authors = Column("Source", String)
    year = Column("Year", String)
    rank = Column("Rank", String)
    origin = Column("Origin", String)
    origin_x = Column("OriginX", String)
    used_in = Column("UsedIn", Text)
    TID_old = Column("TID", Integer)  # references


class AccessWordSpell(Base, BaseFunctions):
    """WordSpell model"""
    __tablename__ = "WordSpell"
    sort_name = "WordSpell"

    word_id = Column("WID", Integer, nullable=False)
    word = Column("Word", String, nullable=False)
    sort_a = Column("SortA", String, nullable=False)
    sort_b = Column("SortB", String, nullable=False)
    event_start_id = Column("SEVT", Integer, nullable=False)
    event_end_id = Column("EEVT", Integer, nullable=False)
    origin_x = Column("OriginX", String)
    id = Column(Integer, primary_key=True)


'''
class AccessXWord(Base, BaseFunctions):
    """XWord model"""
    __tablename__ = "XWord"
    sort_name = "XWord"

    XSortA = Column(String)
    XSortB = Column(String)
    WID = Column(String, primary_key=True)
    I = Column(String)
    XWord = Column(String)
'''

models_ac = (
    AccessAuthor, AccessDefinition, AccessEvent, AccessSetting,
    AccessSyllable, AccessType, AccessWordSpell, AccessWord, )
