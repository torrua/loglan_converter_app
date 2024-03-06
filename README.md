> [!CAUTION]
> Loi, logli! This application and repository are no longer supported. To convert [loglan dictionary data](https://github.com/torrua/LOD) into different formats, please use the [Loglan Database Converter CLI Tool](https://github.com/torrua/loglan_convert).


# Loglan ♻️ Converter
## Description
The **Loglan Converter** project allows you to import Loglan dictionary from text files into a databases, and vice versa - export from an Access (*.mdb file) or remote database back to text files or even directly move from db to another. 

Origin text files are available for downloading from the **LOD** [project materials](https://raw.githubusercontent.com/torrua/LOD/master/tables/). Since program automatically downloads latest ones, it is possible but not necessary to do it manually.

## How to use
Using this program is simple. Just run the **Loglan DB Converter.exe** file, fill in the required fields and push the button with the desired conversion process. The additionally opened command line console will display the progress of the conversion.

![Main Window](https://telegra.ph/file/ac1746b2210f73164ec31.png)

*Files, Console and App Window*

## Download data
Starting from scratch, you will need to download the dictionary data from the internet. This can be done by clicking on the "Download filled MDB file" or "Download text files" buttons. It is also possible to use the "Use text files from Github" option to load raw data directly without saving files.

## Configuration
* DB URI - the [Postgres] db connection URI  (local or remote)
* Access Path - the local Microsoft Access database file path (*.mdb)
* Export to - the directory where exported files will be located
* Import from - the directory where files for import are located

## How to convert 
✔️Always use the [latest *.mdb file](https://github.com/torrua/LOD/raw/master/source/LoglanDictionary.mdb) from from the **LOD** project for full data compatibility.<br>
⚠️All existing tables in the destination database completely delete during importing!<br>
By default, the Postgres database is used, but you can configure any other supported by SQLAlchemy.<br>
After starting the conversion process, the application may freeze for a while - this is normal behavior.<br>
### from txt → db
To import dictionary data from text files into a database, you must first define **Import from** (or select "Use text files from Github") and **DB URI**.

_This process is the longest of all due to the complexity of the data structure. The duration can be up to 30 minutes (or even longer) depending on the performance of the computer._
### from db → txt
To import dictionary data from database into text files, you must first define **Export to** (./export by default) and **DB URI** where dictionary data located.
### from txt → access
To import dictionary data from text files into an Access file, you must first define **Import from** (or select "Use text files from Github") and **Access Path**.
### from access → txt
To import dictionary data from an Access file to text files, you must first define **Export to** (./export by default) and **Access Path**.
### from access → db
To import dictionary data from database into an Access file, you must first define **DB URI** and **Access Path**. 
### from db → access
To import dictionary data from an Access file into database, you must first define **DB URI** and **Access Path**.
