# -*- coding: utf-8 -*-
"""
Export extensions of LOD database models
Add export() function to db object for returning its text string presentation
"""

from config.access.model_dictionary import AccessAuthor, AccessEvent, \
    AccessSetting, AccessSyllable, AccessType, AccessWord, AccessDefinition, AccessWordSpell


class ExportAuthor(AccessAuthor):
    def export(self):
        return f"{self.abbreviation}@{self.full_name}@{self.notes if self.notes else ''}"


class ExportEvent(AccessEvent):
    def export(self):
        #  .strftime('%m/%d/%Y')
        return f"{self.id}@{self.name}" \
               f"@{self.date}@{self.definition}" \
               f"@{self.annotation if self.annotation else ''}" \
               f"@{self.suffix if self.suffix else ''}"


class ExportSyllable(AccessSyllable):
    def export(self):
        return f"{self.name}@{self.type}@{self.allowed}"


class ExportSetting(AccessSetting):
    def export(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}@{self.db_version}@{self.last_word_id}"


class ExportType(AccessType):
    def export(self):
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}"


class ExportWord(AccessWord):
    def export(self):
        """
                Prepare Word data for exporting to text file
                :return: Formatted basic string
                """

        return f"{self.word_id}@{self.type}@{self.type_x}" \
               f"@{self.affixes if self.affixes else ''}" \
               f"@{self.match if self.match else ''}" \
               f"@{self.authors}@{self.year}" \
               f"@{self.rank if self.rank else ''}" \
               f"@{self.origin if self.origin else ''}" \
               f"@{self.origin_x if self.origin_x else ''}" \
               f"@{self.used_in if self.used_in else ''}" \
               f"@{self.TID_old if self.TID_old else ''}"


class ExportWordSpell(AccessWordSpell):
    def export(self):
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.word])
        return f"{self.word_id}@{self.word}@{self.word.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id}@{self.origin_x if self.origin_x else ''}"


class ExportDefinition(AccessDefinition):
    def export(self):
        return f"{self.word_id}@{self.position}@{self.usage if self.usage else ''}" \
               f"@{self.grammar if self.grammar else ''}" \
               f"@{self.body}@@{self.case_tags if self.case_tags else ''}"


export_models_ac = (
    ExportAuthor, ExportDefinition, ExportEvent, ExportSetting,
    ExportSyllable, ExportType, ExportWordSpell, ExportWord, )
