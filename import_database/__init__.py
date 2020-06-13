# -*- coding: utf-8 -*-
from app.model_dictionary import Author, Key, Event, Setting, Syllable, Word, Definition, Type, WordSpell, XWord
from app import db, SEPARATOR, DEFAULT_LANGUAGE
from config import log

models = (Author, Event, Key, Setting, Syllable, Type, Word, Definition,)