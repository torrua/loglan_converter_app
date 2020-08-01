# -*- coding: utf-8 -*-
"""
Export extensions of LOD database models
Add export() function to db object for returning its text string presentation
"""

from config.postgres.model_dictionary import ComplexAuthor, ComplexEvent, ComplexSyllable, ComplexSetting, ComplexType, ComplexWord, ComplexDefinition


class ExportComplexAuthor(ComplexAuthor):
    def export(self):
        return f"{self.abbreviation}@{self.full_name}@{self.notes}"


class ExportComplexEvent(ComplexEvent):
    def export(self):
        return f"{self.id}@{self.name}" \
               f"@{self.date.strftime('%m/%d/%Y')}@{self.definition}" \
               f"@{self.annotation}@{self.suffix}"


class ExportComplexSyllable(ComplexSyllable):
    def export(self):
        return f"{self.name}@{self.type}@{self.allowed}"


class ExportComplexSetting(ComplexSetting):
    def export(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}@{self.db_version}@{self.last_word_id}@{self.db_release}"


class ExportComplexType(ComplexType):
    def export(self):
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}"


class ExportComplexWord(ComplexWord):
    def export(self):
        """
                Prepare Word data for exporting to text file
                :return: Formatted basic string
                """
        notes = self.notes if self.notes else {}

        w_affixes = self.get_afx()
        affixes = ' '.join(sorted({afx.name.replace("-", "") for afx in w_affixes})) if w_affixes else ""

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
        usedin = ' | '.join(sorted({cpx.name for cpx in w_usedin})) if w_usedin else ""

        tid_old = self.TID_old if self.TID_old else ""
        origin_x = self.origin_x if self.origin_x else ""
        origin = self.origin if self.origin else ""
        return f"{self.id_old}@{self.type.type}@{self.type.type_x}@{affixes}" \
               f"@{match}@{source}@{year}@{rank}" \
               f"@{origin}@{origin_x}@{usedin}@{tid_old}"


class ExportComplexDefinition(ComplexDefinition):
    def export(self):
        return f"{self.source_word.id_old}@{self.position}@{self.usage if self.usage else ''}" \
               f"@{self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''}" \
               f"@{self.body}@@{self.case_tags if self.case_tags else ''}"


class ExportComplexWordSpell(ComplexWord):
    def export(self):
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.name])

        return f"{self.id_old}@{self.name}@{self.name.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id if self.event_end else 9999}@"


export_models_pg = (
    ExportComplexAuthor, ExportComplexDefinition, ExportComplexEvent, ExportComplexSetting,
    ExportComplexSyllable, ExportComplexType, ExportComplexWord, ExportComplexWordSpell, )
