# -*- coding: utf-8 -*-
"""
Import Text Files Variables
"""
import os
from config import root_directory

IMPORT_DIRECTORY_PATH_REMOTE = os.getenv(
    "IMPORT_DIRECTORY_PATH_REMOTE",
    "https://raw.githubusercontent.com/torrua/LOD/master/tables/")
IMPORT_DIRECTORY_PATH_LOCAL = os.getenv("IMPORT_DIRECTORY_PATH_LOCAL", f"{root_directory}import\\")
