# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime
import datetime as dt

import pytest

from config.postgres.model_base import BaseWord as Word, BaseType as Type, BaseEvent as Event, \
    BaseAuthor as Author, BaseDefinition as Definition, BaseKey as Key, BaseSetting as Setting, \
    BaseSyllable as Syllable, BaseWordSource as WordSource

from tests.functions import db_add_objects, db_connect_authors, db_connect_keys, db_connect_words

from tests.data import keys, definitions, words, types, authors, settings, syllables
from tests.data import changed_words, changed_events, all_events, doubled_words
from tests.data import littles, little_types
from tests.data import definition_1, definition_2, word_1, word_2, word_3

from tests.data import connect_authors
from tests.data import connect_keys
from tests.data import connect_words


@pytest.mark.usefixtures("db")
class TestAuthor:
    """Author tests."""
    @pytest.mark.parametrize("item", authors)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        author = Author(**item)
        author.save()
        author_from_db = Author.get_by_id(item["id"])

        assert type(author) == Author
        assert author == author_from_db
        assert type(author.id) == int
        assert type(author.abbreviation) == str
        assert isinstance(author.full_name, (str, type(None)))
        assert isinstance(author.notes, (str, type(None)))

    def test_relationship_contribution(self):
        db_add_objects(Author, authors)
        db_add_objects(Word, words)
        db_connect_authors(connect_authors)

        test_author = Author.get_by_id(29)
        assert len(test_author.contribution) == 3
        assert isinstance(test_author.contribution, list)
        assert [w.name for w in test_author.contribution] == ['kakto', 'pruci', 'prukao']

        test_author = Author.get_by_id(13)
        assert len(test_author.contribution) == 3
        assert [w.name for w in test_author.contribution] == ['kak', 'kao', 'pru']


@pytest.mark.usefixtures("db")
class TestEvent:
    """Event tests."""

    @pytest.mark.parametrize("item", all_events)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        event = Event(**item)
        event.save()
        event_from_db = Event.get_by_id(item["id"])

        assert event == event_from_db
        assert isinstance(event, Event)
        assert isinstance(event.id, int)
        assert isinstance(event.date, datetime.date)
        assert isinstance(event.name, str)
        assert isinstance(event.definition, str)
        assert isinstance(event.annotation, str)
        assert isinstance(event.suffix, str)

    def test_relationship_deprecated_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.appeared_words, list)
        assert len(event.appeared_words) == 3

    def test_relationship_appeared_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.deprecated_words, list)
        assert len(event.deprecated_words) == 4

    def test_latest(self):
        db_add_objects(Event, all_events)
        latest = Event.latest()

        assert latest.id == 6
        assert latest.annotation == 'Torrua Repair'


@pytest.mark.usefixtures("db")
class TestKey:
    """Key tests."""

    @pytest.mark.parametrize("item", keys)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        key = Key(**item)
        key.save()
        key_from_db = Key.get_by_id(item["id"])

        assert key == key_from_db
        assert isinstance(key, Key)
        assert isinstance(key.id, int)
        assert isinstance(key.word, str)
        assert isinstance(key.language, (str, type(None)))

    def test_relationship_definitions(self):
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)
        key = Key.get_by_id(12474)

        assert isinstance(key.definitions, list)
        assert len(key.definitions) == 5
        assert [d.id for d in key.definitions] == [13521, 13523, 13524, 13527, 13531]


@pytest.mark.usefixtures("db")
class TestSetting:
    """Setting tests."""

    @pytest.mark.parametrize("item", settings)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        setting = Setting(**item)
        setting.save()
        setting_from_db = Setting.get_by_id(item["id"])

        assert setting == setting_from_db
        assert isinstance(setting, Setting)
        assert isinstance(setting.id, int)
        assert isinstance(setting.date, (datetime.datetime, type(None)))
        assert isinstance(setting.db_version, int)
        assert isinstance(setting.last_word_id, int)
        assert isinstance(setting.db_release, str)


@pytest.mark.usefixtures("db")
class TestSyllable:
    """Syllable tests."""

    @pytest.mark.parametrize("item", syllables)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        syllable = Syllable(**item)
        syllable.save()
        syllable_from_db = Syllable.get_by_id(item["id"])

        assert syllable == syllable_from_db
        assert isinstance(syllable, Syllable)
        assert isinstance(syllable.id, int)
        assert isinstance(syllable.name, str)
        assert isinstance(syllable.type, str)
        assert isinstance(syllable.allowed, (bool, type(None)))


@pytest.mark.usefixtures("db")
class TestType:
    """Type tests."""

    @pytest.mark.parametrize("item", types)
    def test_create_from_dict_with_data(self, item):
        type_ = Type(**item)
        type_.save()
        type_from_db = Type.get_by_id(item["id"])

        assert type_ == type_from_db
        assert isinstance(type_.id, int)
        assert isinstance(type_.type, str)
        assert isinstance(type_.type_x, str)
        assert isinstance(type_.group, (str, type(None)))
        assert isinstance(type_.parentable, bool)
        assert isinstance(type_.description, (str, type(None)))
        with pytest.raises(Exception) as _:
            assert type_.type == "A-Prim"

    def test_query_by(self):
        db_add_objects(Type, types)

        test_type = Type.query_by("Predicate").count()
        assert test_type == 2

        test_type = Type.query_by("Predicate").all()
        assert len(test_type) == 2

        test_type = Type.query_by("Afx").first()
        assert test_type.group == "Little"

    def test_by(self):
        db_add_objects(Type, types)
        test_type = Type.by("Little", only_first=True)
        assert test_type.type == "Afx"

        test_type = Type.by("Little")
        assert test_type[0].type == "Afx"

        test_type = Type.by("2-Cpx", only_first=True)
        assert test_type.group == "Cpx"

        test_type = Type.by("Predicate")
        assert len(test_type) == 2

    def test_relationship_words(self):
        db_add_objects(Type, types)
        db_add_objects(Word, words)

        test_type = Type.by("Little", only_first=True)
        assert len(test_type.words) == 3

        test_type = Type.by("C-Prim", only_first=True)
        assert len(test_type.words) == 2

        test_type = Type.by("Cpx", only_first=True)
        assert len(test_type.words) == 1


@pytest.mark.usefixtures("db")
class TestDefinition:
    """Definition tests."""

    @pytest.mark.parametrize("item", definitions)
    def test_create_from_dict_with_data(self, item):
        definition = Definition(**item)
        definition.save()
        definition_from_db = Definition.get_by_id(item["id"])

        assert definition == definition_from_db
        assert isinstance(definition.id, int)
        assert isinstance(definition.word_id, int)
        assert isinstance(definition.position, int)
        assert isinstance(definition.usage, (str, type(None)))
        assert isinstance(definition.grammar_code, (str, type(None)))
        assert isinstance(definition.slots, (int, type(None)))
        assert isinstance(definition.case_tags, (str, type(None)))
        assert isinstance(definition.body, str)
        assert isinstance(definition.language, (str, type(None)))
        assert isinstance(definition.notes, (str, type(None)))

    def test_relationship_keys(self):
        pass

    def test_relationship_source_word(self):
        pass

    def test_grammar(self):
        db_add_objects(Definition, definitions)
        d = Definition.get_by_id(13527)
        assert d.grammar == "(4v)"

        d = Definition.get_by_id(13529)
        assert d.grammar == "(a)"

    def test_link_keys_from_list_of_str(self):
        db_add_objects(Definition, definitions)
        db_add_objects(Key, keys)

        keys_to_add = ["test", "examine"]
        d = Definition.get_by_id(13527)
        assert d.keys.count() == 0

        d.link_keys_from_list_of_str(keys_to_add)
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(keys_to_add)

    def test_link_key_from_str(self):
        db_add_objects(Key, keys)
        d = Definition(**definition_2)
        d.save()
        assert d.keys.count() == 0

        key_to_add = "tester"
        d.link_key_from_str(key_to_add)
        assert d.keys.count() == 1
        assert d.keys.first().word == key_to_add

    """
    def test_link_keys_from_list_of_obj(self):
        # TODO fix bug if keys already exist in db
        d = Definition(**definition_2)
        d.save()
        assert d.keys.count() == 0
        keys_to_add = [Key(**k) for k in keys[:5]]
        d.link_keys_from_list_of_obj(keys_to_add)
        assert d.keys.count() == 5

        d.link_keys_from_list_of_obj(keys_to_add)
        assert d.keys.count() == 5

    def test_link_key_from_obj(self):
        # TODO fix bug if key already exists in db

        d = Definition(**definition_2)
        d.save()
        assert d.keys.count() == 0

        key_to_add = Key(**keys[1])
        d.link_key_from_obj(key_to_add)
        assert d.keys.count() == 1
    """

    def test_link_keys_from_definition_body(self):
        db_add_objects(Key, keys)
        d = Definition(**definition_1)

        d.save()
        assert d.keys.count() == 0

        d.link_keys_from_definition_body()
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(["test", "examine"])

    def test_link_keys(self):
        db_add_objects(Key, keys)
        keys_to_add_str = ["test", "examine"]
        key_to_add_str = "tester"

        d0 = Definition(**definitions[0])
        d0.save()
        assert d0.keys.count() == 0

        d0.link_keys(keys_to_add_str)
        assert d0.keys.count() == 2

        d1 = Definition(**definitions[1])
        d1.save()
        assert d1.keys.count() == 0

        d1.link_keys(key_to_add_str)
        assert d1.keys.count() == 1

        # TODO
        """
        keys_to_add = [Key(**k) for k in keys[:5]]
        key_to_add = Key(**keys[1])

        d2 = Definition(**definitions[2])
        d2.save()
        assert d2.keys.count() == 0

        d2.link_keys(keys_to_add)
        assert d2.keys.count() == 5

        d3 = Definition(**definitions[3])
        d3.save()
        assert d3.keys.count() == 0

        d3.link_keys(key_to_add)
        assert d3.keys.count() == 1
        """


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    @pytest.mark.parametrize("item", words)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""
        word = Word(**item)
        word.save()
        word_from_db = Word.get_by_id(item["id"])

        assert word == word_from_db
        assert isinstance(word.id, int)
        assert isinstance(word.id_old, int)
        assert isinstance(word.name, str)
        assert isinstance(word.origin, (str, type(None)))
        assert isinstance(word.origin_x, (str, type(None)))
        assert isinstance(word.match, (str, type(None)))
        assert isinstance(word.rank, (str, type(None)))
        assert isinstance(word.year, (dt.date, type(None)))
        assert isinstance(word.notes, (dict, type(None)))
        assert isinstance(word.TID_old, (int, type(None)))

    @pytest.mark.parametrize("item", words)
    def test_type_relationship(self, item):
        word = Word(**item)
        word.save()

        type_data = [t for t in types if t["id"] == word.type_id][0]
        type_ = Type(**type_data)
        type_.save()

        type_from_db = Type.get_by_id(word.type_id)

        assert type(type_) == type(type_from_db) == Type
        assert type_from_db == type_ == word.type

    @pytest.mark.parametrize("item", words)
    def test_event_relationship(self, item):
        db_add_objects(Event, all_events)
        word = Word(**item)
        word.save()

        event_start_from_db = Event.get_by_id(word.event_start_id)
        assert type(event_start_from_db) == Event
        assert event_start_from_db == word.event_start

        if word.event_end_id:
            event_end_from_db = Event.get_by_id(word.event_end_id)
            assert isinstance(event_end_from_db, Event)
            assert event_end_from_db == word.event_start
        else:
            assert word.event_end is None

    def test_authors_relationship(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)
        db_connect_authors(connect_authors)

        word = Word.get_by_id(7316)
        author = Author.get_by_id(29)

        assert word.authors.count() == 1
        assert word.authors[0] == author

    def test_definitions_relationship(self):
        word = Word(**word_1)
        word.save()
        definitions_to_add = [d for d in definitions if d["word_id"] == word.id]
        db_add_objects(Definition, definitions_to_add)

        assert word.definitions.count() == len(definitions_to_add) == 5
        assert isinstance(word.definitions[0], Definition)

    def test_add_child(self):
        db_add_objects(Word, words)
        cmp = Word.get_by_id(word_1.get("id"))
        assert cmp._parents.count() == 0

        for p in [word_2, word_3]:
            prim = Word.get_by_id(p.get("id"))
            prim.add_child(cmp)

        assert cmp._parents.count() == 2

    def test_add_children(self):
        db_add_objects(Word, words)
        cmp = Word.get_by_id(word_1.get("id"))
        assert cmp._parents.count() == 0

        for p in [word_2, word_3]:
            prim = Word.get_by_id(p.get("id"))
            prim.add_children([cmp, ])

        assert cmp._parents.count() == 2

    def test_add_author(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)

        word = Word.get_by_id(7316)
        author = Author.get_by_id(29)
        assert word.authors.count() == 0

        word.add_author(author)
        assert word.authors.count() == 1
        assert word.authors[0] == author

        word.add_author(author)
        assert word.authors.count() == 1

    def test_add_authors(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)

        word = Word.get_by_id(7316)
        assert word.authors.count() == 0

        local_authors = Author.get_all()
        word.add_authors(local_authors)

        assert word.authors.count() == 2
        assert isinstance(word.authors[0], Author)

    def test_query_derivatives(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_derivatives().count() == 3
        assert p2.query_derivatives().count() == 2
        assert isinstance(p2.query_derivatives().first(), Word)

    def test_query_parents(self):
        db_add_objects(Word, words)
        db_connect_words(connect_words)

        cmp = Word.get_by_id(7316)

        assert cmp.query_parents().count() == 2
        assert isinstance(cmp.query_parents().first(), Word)

    def test_query_cpx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_cpx().count() == 1
        assert p2.query_cpx().count() == 1

    def test_query_afx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_afx().count() == 2
        assert p2.query_afx().count() == 1

    def test_query_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).query_keys().count()

        assert result == 7

    def test_parents(self):
        db_add_objects(Word, words)
        db_connect_words(connect_words)

        result = Word.get_by_id(7316).parents

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_complexes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).complexes

        assert len(result) == 1
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_affixes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).affixes

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).keys

        assert len(result) == 6
        assert isinstance(result, list)
        assert isinstance(result[0], Key)

    def test_get_sources_prim(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)

        afx = Word.get_by_id(3802)
        assert afx.get_sources_prim() == []

        result = Word.get_by_id(3813).get_sources_prim()
        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)

    def test__get_sources_c_prim(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)

        result = Word.get_by_id(3813)._get_sources_c_prim()

        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)

    def test_get_sources_cpx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)

        result = Word.get_by_id(7316).get_sources_cpx()
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = Word.get_by_id(7316).get_sources_cpx(as_str=True)
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert result == ['pruci', 'kakto', ]

        result = Word.get_by_id(3813).get_sources_cpx()
        assert result == []

    def test_get_sources_cpd(self):
        db_add_objects(Word, littles)
        db_add_objects(Type, little_types)

        result = Word.get_by_id(479).get_sources_cpd()
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = Word.get_by_id(479).get_sources_cpd(as_str=True)
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert result == ['bi', 'cio']

    def test_by_event(self):
        db_add_objects(Word, changed_words + words)
        db_add_objects(Event, all_events)

        result = Word.get_all()
        assert len(result) == 13

        result = Word.by_event(1).all()
        assert len(result) == 10

        result = Word.by_event(5).all()
        assert len(result) == 9

    def test_by_name(self):
        db_add_objects(Word, doubled_words)

        result = Word.by_name("duo").count()
        assert result == 2

        result = Word.by_name("duo").all()
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = sorted([w.type_id for w in result])
        assert result == [2, 17]

        result = Word.by_name("duo").first()
        assert isinstance(result, Word)

    def test_by_key(self):
        db_add_objects(Word, words)
        db_add_objects(Definition, definitions)
        db_add_objects(Key, keys)
        db_connect_keys(connect_keys)

        result = Word.by_key("test").count()
        assert result == 5

        result = [w.name for w in Word.by_key("test").all()]
        assert result == ['pru', 'pruci', 'prukao']
