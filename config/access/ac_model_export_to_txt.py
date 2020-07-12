# -*- coding: utf-8 -*-
"""
Export extensions of LOD database models
Add export() function to db object for returning its text string presentation
"""
import ast
from datetime import datetime
from typing import List
from config.access.model_dictionary import AccessAuthor, AccessEvent, \
    AccessSetting, AccessSyllable, AccessType, AccessWord, AccessDefinition, AccessWordSpell


class IOAuthor(AccessAuthor):
    def export(self):
        return f"{self.abbreviation}@{self.full_name}@{self.notes if self.notes else ''}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "abbreviation": item[0],
            "full_name": item[1] if item[1] else None,
            "notes": item[2] if item[2] else None
        }


class IOEvent(AccessEvent):
    def export(self):
        #  .strftime('%m/%d/%Y')
        return f"{self.id}@{self.name}" \
               f"@{self.date}@{self.definition}" \
               f"@{self.annotation if self.annotation else ''}" \
               f"@{self.suffix if self.suffix else ''}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "id": int(item[0]),
            "name": item[1],
            "date": item[2],
            "definition": item[3],
            "annotation": item[4] if item[4] else None,
            "suffix": item[5] if item[5] else None,
        }


class IOSyllable(AccessSyllable):
    def export(self):
        return f"{self.name}@{self.type}@{self.allowed}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "name": item[0],
            "type": item[1],
            "allowed": ast.literal_eval(item[2]) if item[2] else False,
        }


class IOSetting(AccessSetting):
    def export(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}" \
               f"@{self.db_version}@{self.last_word_id}@{self.db_release}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "date": datetime.strptime(item[0], '%d.%m.%Y %H:%M:%S'),
            "db_version": int(item[1]),
            "last_word_id": int(item[2]),
            "db_release": item[3],
        }


class IOType(AccessType):
    def export(self):
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "type": item[0],
            "type_x": item[1],
            "group": item[2] if item[2] else None,
            "parentable": ast.literal_eval(item[3]),
        }


class IOWord(AccessWord):
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

    @staticmethod
    def import_(item: List[str]):
        return {
            "word_id": int(item[0]),
            "type": item[1],
            "type_x": item[2],
            "affixes": item[3] if item[3] else None,
            "match": item[4] if item[4] else None,
            "authors": item[5] if item[5] else None,
            "year": item[6] if item[6] else None,
            "rank": item[7] if item[7] else None,
            "origin": item[8] if item[8] else None,
            "origin_x": item[9] if item[9] else None,
            "used_in": item[10] if item[10] else None,
            "TID_old": int(item[11]) if item[11] else None,
        }


class IOWordSpell(AccessWordSpell):
    def export(self):
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.word])
        return f"{self.word_id}@{self.word}@{self.word.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id}@{self.origin_x if self.origin_x else ''}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "word_id": int(item[0]),
            "word": item[1],
            "sort_a": item[2],
            "sort_b": item[3],
            "event_start_id": int(item[4]),
            "event_end_id": int(item[5]),
            "origin_x": item[6] if item[6] else None,
        }


class IODefinition(AccessDefinition):
    def export(self):
        return f"{self.word_id}@{self.position}@{self.usage if self.usage else ''}" \
               f"@{self.grammar if self.grammar else ''}" \
               f"@{self.body}@@{self.case_tags if self.case_tags else ''}"

    @staticmethod
    def import_(item: List[str]):
        return {
            "word_id": int(item[0]),
            "position": int(item[1]),
            "usage": item[2] if item[2] else None,
            "grammar": item[3] if item[3] else None,
            "body": item[4],
            "main": item[5] if item[5] else None,
            "case_tags": item[6] if item[6] else None,
        }


export_models_ac = (
    IOAuthor, IODefinition, IOEvent, IOSetting,
    IOSyllable, IOType, IOWord, IOWordSpell, )
