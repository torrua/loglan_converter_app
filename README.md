# Loglan ♻️ Converter
## Description
The **Loglan Converter** project allows you to import Loglan dictionary from text files into a database, and vice versa - export from a database back to text files. Origin text files are available for download in the **LOD** project [materials](https://raw.githubusercontent.com/torrua/LOD/master/tables/).
The program automatically downloads latest ones, so it is not necessary to do it manually.

## How to import (txt → db)
To import dictionary data into a database, you must first define the environment variable ``LOD_DATABASE_URL`` with target database URI. By default, the Postgres database is used, but you can configure any other supported by SQLAlchemy.

⚠️ All existing tables in the database will be completely deleted before importing.

Call the function ``import_database.db_functions_generate.db_recreate_db()`` to start the import process.

## How to export (db → txt)
To export data from the dictionary back to text files, you must first define the environment variable ``LOD_DATABASE_URL`` with the dictionary database URI, the variable ``EXPORT_DIRECTORY_PATH`` with the export folder location and a set of variables with filenames (``FILE_NAME_AUTHOR``, ``FILE_NAME_LEXEVENT``, ``FILE_NAME_PERMISSIBLEINITIALCC``, ``FILE_NAME_SETTINGS``, ``FILE_NAME_TYPE``, ``FILE_NAME_WORDDEFINITION``, ``FILE_NAME_WORDS``, ``FILE_NAME_WORDSPELL`` and ``FILE_NAME_XWORD``).

⚠️ All existing files in the export folder with matching names will be overwritten during export.

Call the function``export_database.db_functions_export.export_db()`` to start the export process.
