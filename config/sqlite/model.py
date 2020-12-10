# -*- coding: utf-8 -*-

"""
Models of Translation database
"""
from __future__ import annotations

from typing import List

from sqlalchemy.orm import synonym

from loglan_db.model_init import InitBase, DBBase
from config.sqlite import db

T_NAME_KEYS = "keys"
T_NAME_MEANINGS = "meanings"

db.metadata.clear()


class Key(db.Model, InitBase, DBBase):
    """Key model"""
    __tablename__ = T_NAME_KEYS

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(16))

    def add_meaning(self, meaning: Meaning) -> str:
        """
        Connect Meaning object with Key object
        :param meaning: Meaning object
        :return:
        """
        if not self.meanings.filter(Meaning.translation == meaning.translation).count() > 0:
            self.meanings.append(meaning)
            db.session.commit()
        return meaning.translation

    def add_meanings(self, meanings: List[Meaning]):
        """
        Connect Meaning objects with Key object
        :param meanings: List of Meaning object
        :return:
        """
        new_meanings = list(set(meanings) - set(self.meanings))
        _ = self.meanings.extend(new_meanings) if new_meanings else None
        db.session.commit()


class Meaning(db.Model, InitBase, DBBase):
    """Meaning model"""
    __tablename__ = T_NAME_MEANINGS

    id = db.Column(db.Integer, primary_key=True)
    translation = db.Column(db.String, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(16), nullable=False)
    _part_of_speech = db.Column(db.String, nullable=True)

    @property
    def part_of_speech(self):
        """getter"""
        return self._part_of_speech.split(" | ") if self._part_of_speech else []

    @part_of_speech.setter
    def part_of_speech(self, value):
        """setter"""
        self._part_of_speech = " | ".join(value) if value else None

    part_of_speech = synonym('_part_of_speech', descriptor=part_of_speech)

    source_word = db.Column("source_word", db.ForeignKey(f'{T_NAME_KEYS}.word'))
    key = db.relationship(Key, foreign_keys=[source_word], backref="meanings")
