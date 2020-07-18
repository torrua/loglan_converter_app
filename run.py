# -*- coding: utf-8 -*-
from converters.ac_to_txt import convert_ac_to_txt
from converters.ac_to_pg import convert_ac_to_pg

from converters.pg_to_txt import convert_pg_to_txt
from converters.pg_to_ac import convert_pg_to_ac

from converters.txt_to_pg import convert_txt_to_pg
from converters.txt_to_ac import convert_txt_to_ac

# TODO Activate source selection
#   TODO fix txt export paths
#   TODO fix txt import paths

# TODO Unify logging and resulting

SELECTOR = 4

if __name__ == "__main__":

    from config import create_app
    from config.postgres import CLIConfig

    with create_app(CLIConfig).app_context():
        if SELECTOR == 1:
            convert_ac_to_txt()

        elif SELECTOR == 2:
            convert_ac_to_pg()

        elif SELECTOR == 3:
            convert_pg_to_txt()

        elif SELECTOR == 4:
            convert_pg_to_ac()

        elif SELECTOR == 5:
            convert_txt_to_ac()

        else:
            convert_txt_to_pg()
