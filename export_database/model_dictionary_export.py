# -*- coding: utf-8 -*-
"""
Export extensions of LOD database models
Add export() function to db object for returning its text string presentation
"""

from export_database import Author, Event, Syllable, Setting, Type, Word, Definition


class ExportAuthor(Author):
    def export(self):
        return f"{self.abbreviation}@{self.full_name}@{self.notes}"


class ExportEvent(Event):
    def export(self):
        return f"{self.id}@{self.name}" \
               f"@{self.date.strftime('%m/%d/%Y')}@{self.definition}" \
               f"@{self.annotation}@{self.suffix}"


class ExportSyllable(Syllable):
    def export(self):
        return f"{self.name}"


class ExportSetting(Setting):
    def export(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}@{self.db_version}@{self.last_word_id}"


class ExportType(Type):
    def export(self):
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}"


class ExportWord(Word):
    def export(self):
        """
                Prepare Word data for exporting to text file
                :return: Formatted basic string
                """
        notes = self.notes if self.notes else {}

        w_affixes = self.get_afx()
        affixes = ' '.join(sorted([afx.name for afx in w_affixes])) if w_affixes else ""

        w_match = self.match
        match = w_match if w_match else ""

        w_source = self.authors.all()
        # print(self) if not self.authors.all() else None
        source = '/'.join(sorted([auth.abbreviation for auth in w_source])) \
            if len(w_source) > 1 else w_source[0].abbreviation
        source = source + (" " + notes["author"] if notes.get("author", False) else "")

        year = str(self.year.year) + (" " + notes["year"] if notes.get("year", False) else "")

        rank = self.rank + (" " + notes["rank"] if notes.get("rank", False) else "")

        w_usedin = self.get_cpx()
        usedin = ' | '.join(sorted([cpx.name for cpx in w_usedin])) if w_usedin else ""

        tid_old = self.TID_old if self.TID_old else ""

        return f"{self.id_old}@{self.type.type}@{self.type.type_x}@{affixes}" \
               f"@{match}@{source}@{year}@{rank}" \
               f"@{self.origin}@{self.origin_x}@{usedin}@{tid_old}"

    @property
    def export_spell_as_string(self) -> str:
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.name])

        return f"{self.id_old}@{self.name}@{self.name.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id if self.event_end else 9999}@"


class ExportDefinition(Definition):
    def export(self):
        return f"{self.source_word.id_old}@{self.position}@{self.usage}" \
               f"@{self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''}" \
               f"@{self.body}@@{self.case_tags}"
