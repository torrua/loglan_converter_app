from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime

from config.access import Base
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class BaseFunctions:
    """
    Base class for common methods
    """
    __tablename__ = None

    @declared_attr
    def import_file_name(cls):
        return f"{cls.__tablename__}.txt"

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

    @classmethod
    def export_file_path(cls, export_directory):
        return export_directory + cls.export_file_name

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
    full_name = Column(String(64))
    notes = Column(String(128))


class AccessDefinition(Base, BaseFunctions):
    __tablename__ = 'WordDefinition'
    sort_name = "Definition"

    word_id = Column("WID", Integer, primary_key=True)
    position = Column("I", Integer, nullable=False)
    usage = Column("Usage", String(64))
    grammar = Column("Grammar", String(8))
    body = Column("Definition", Text, nullable=False)
    main = Column("Main", String(8))
    case_tags = Column("Tags", String(16))


class AccessEvent(Base, BaseFunctions):
    """
    Event model
    """
    __tablename__ = "LexEvent"
    sort_name = "Event"

    id = Column("EVT", Integer, primary_key=True)
    name = Column("Event", String(64), nullable=False)
    date = Column("When", String(32), nullable=False)
    definition = Column("WhyWhat", Text, nullable=False)
    annotation = Column("DictionaryAnnotation", String(16))
    suffix = Column("FilenameSuffix", String(16))


class AccessSetting(Base, BaseFunctions):
    """
    Setting model
    """
    __tablename__ = "Settings"
    sort_name = "Settings"

    date = Column("DateModified", DateTime,  primary_key=True)
    db_version = Column("DBVersion", Integer, nullable=False)
    last_word_id = Column("LastWID", Integer, nullable=False)
    db_release = Column("DBRelease", String(16), nullable=False)


class AccessSyllable(Base, BaseFunctions):
    """
    Syllable model
    """
    __tablename__ = "Syllable"
    sort_name = "Syllable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("characters", String(8), primary_key=True)
    type = Column(String(32), nullable=False)
    allowed = Column(Boolean)


class AccessType(Base, BaseFunctions):
    """
    Type model
    """
    __tablename__ = "Type"
    sort_name = "Type"

    id = Column(Integer, primary_key=True)
    type = Column(String(16), nullable=False)
    type_x = Column(String(16), nullable=False)
    group = Column(String(16), nullable=False)
    parentable = Column(Boolean, nullable=False)


class AccessWord(Base, BaseFunctions):
    """
    Word model
    """
    __tablename__ = "Words"
    sort_name = "Word"

    word_id = Column("WID", Integer, nullable=False, primary_key=True)
    type = Column("Type", String(16), nullable=False)
    type_x = Column("XType", String(16), nullable=False)
    affixes = Column("Affixes", String(16))
    match = Column("Match", String(8))
    authors = Column("Source", String(64))
    year = Column("Year", String(128))
    rank = Column("Rank", String(128))
    origin = Column("Origin", String(128))
    origin_x = Column("OriginX", String(64))
    used_in = Column("UsedIn", Text)
    TID_old = Column("TID", Integer)  # references


class AccessWordSpell(Base, BaseFunctions):
    """WordSpell model"""
    __tablename__ = "WordSpell"
    sort_name = "WordSpell"

    word_id = Column("WID", Integer, nullable=False)
    word = Column("Word", String(64), nullable=False)
    sort_a = Column("SortA", String(64), nullable=False)
    sort_b = Column("SortB", String(64), nullable=False)
    event_start_id = Column("SEVT", Integer, nullable=False)
    event_end_id = Column("EEVT", Integer, nullable=False)
    origin_x = Column("OriginX", String(64))
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
