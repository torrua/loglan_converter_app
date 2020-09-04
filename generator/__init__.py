# -*- coding: utf-8 -*-
"""
Initial for HTML Generator
"""
from os import environ
from pathlib import Path

HTML_EXPORT_DIRECTORY_PATH_LOCAL = environ.get("HTML_EXPORT_DIRECTORY_PATH_LOCAL", "")

if HTML_EXPORT_DIRECTORY_PATH_LOCAL:
    Path(HTML_EXPORT_DIRECTORY_PATH_LOCAL).mkdir(parents=True, exist_ok=True)
