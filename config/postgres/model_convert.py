# -*- coding: utf-8 -*-
"""
Conversion extensions for basic LOD models
"""

from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr


class ConvertBase:
    """
    Common convert extension for basic LOD models
    """
    __index_sort_import__ = None
    __index_sort_export__ = None
    __load_from_file__ = True
    __load_to_db__ = True
    import_file_name = None

    @declared_attr
    def export_file_name(cls) -> str:
        """
        Generate text file name for export class data
        :return:
        """
        return f"PG_{datetime.now().strftime('%y%m%d%H%M')}_{cls.import_file_name}"

    @classmethod
    def export_file_path(cls, export_directory) -> str:
        """
        Return full file path according export_file_name
        :param export_directory:
        :return:
        """
        return export_directory + cls.export_file_name


class ConvertAuthor(ConvertBase):
    """
    Convert extension for basic Author LOD model
    """
    __index_sort_import__ = 1
    __index_sort_export__ = 1
    import_file_name = "Author.txt"


class ConvertEvent(ConvertBase):
    """
    Convert extension for basic Event LOD model
    """
    __index_sort_import__ = 2
    __index_sort_export__ = 3
    import_file_name = "LexEvent.txt"


class ConvertKey(ConvertBase):
    """
    Convert extension for basic Key LOD model
    """
    __index_sort_import__ = 3
    __index_sort_export__ = 8
    __load_from_file__ = False
    __load_to_db__ = True


class ConvertSetting(ConvertBase):
    """
    Convert extension for basic Setting LOD model
    """
    __index_sort_import__ = 4
    __index_sort_export__ = 4
    import_file_name = "Settings.txt"


class ConvertSyllable(ConvertBase):
    """
    Convert extension for basic Syllable LOD model
    """
    __index_sort_import__ = 5
    __index_sort_export__ = 5
    import_file_name = "Syllable.txt"


class ConvertType(ConvertBase):
    """
    Convert extension for basic Type LOD model
    """
    __index_sort_import__ = 6
    __index_sort_export__ = 6
    import_file_name = "Type.txt"


class ConvertDefinition(ConvertBase):
    """
    Convert extension for basic Definition LOD model
    """
    __index_sort_import__ = 8
    __index_sort_export__ = 2
    import_file_name = "WordDefinition.txt"


class ConvertWord(ConvertBase):
    """
    Convert extension for basic Word LOD model
    """
    __index_sort_import__ = 7
    __index_sort_export__ = 8
    import_file_name = "Words.txt"


class ConvertWordSpell(ConvertBase):
    """
    Convert extension for basic WordSpell LOD model
    """
    __index_sort_import__ = 9
    __index_sort_export__ = 7
    import_file_name = "WordSpell.txt"
    __load_from_file__ = True
    __load_to_db__ = False
