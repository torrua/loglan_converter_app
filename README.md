# Loglan ♻️ Converter
## Description
The **Loglan Converter** project allows you to import Loglan dictionary from text files into a databases, and vice versa - export from an Access (*.mdb file) or remote database back to text files or even directly move from db to another. 

Origin text files are available for downloading from the **LOD** [project materials](https://raw.githubusercontent.com/torrua/LOD/master/tables/). Since program automatically downloads latest ones, it is possible but not necessary to do it manually.

## How to use
Using this program is simple. Just run the **Loglan DB Converter.exe** file, fill in the required fields and push the button with the desired conversion process. The additionally opened command line console will display the progress of the conversion.

![Main Window](https://telegra.ph/file/e82dd02fa11b3a8b30068.png)

*Files, Console and App Window*

## Configuration
* Postgres URI - the [Postgres] db connection URI  (local or remote)
* Access Path - the local Microsoft Access database file path (*.mdb)
* Export Path - the directory where exported files will be located
* Import Path - the directory where files for import are located

## How to convert 
✔️Always use the [latest *.mdb file](https://github.com/torrua/LOD/raw/master/source/LoglanDictionary.mdb) from from the **LOD** project for full data compatibility.
⚠️ All existing tables in the destination database completely delete during importing!
By default, the Postgres database is used, but you can configure any other supported by SQLAlchemy.
After starting the conversion process, the application may freeze for a while - this is normal behavior.
### from txt → db
To import dictionary data from text files into a database, you must first define **Import Path** (or select "Use text files from Github") and **Postgres URI**.
_This process is the longest of all due to the complexity of the data structure. The duration can be up to 30 minutes (or even longer) depending on the performance of the computer._
### from db → txt
To import dictionary data from database into text files, you must first define **Export Path** (./export by default) and **Postgres URI** where dictionary data located.
### from txt → access
To import dictionary data from text files into an Access file, you must first define **Import Path** (or select "Use text files from Github") and **Access Path**.
### from access → txt
To import dictionary data from an Access file to text files, you must first define **Export Path** (./export by default) and **Access Path**.
### from access → db
To import dictionary data from database into an Access file, you must first define **Postgres URI** and **Access Path**. 
### from db → access
To import dictionary data from an Access file into database, you must first define **Postgres URI** and **Access Path**.