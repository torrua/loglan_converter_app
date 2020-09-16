# -*- coding: utf-8 -*-
from converters.ac_to_txt import convert_ac_to_txt
from converters.ac_to_pg import convert_ac_to_pg

from converters.pg_to_txt import convert_pg_to_txt
from converters.pg_to_ac import convert_pg_to_ac

from converters.txt_to_pg import convert_txt_to_pg
from converters.txt_to_ac import convert_txt_to_ac

# TODO Unify logging and resulting
# TODO Add functions for C-Prim words for find vernaculars
# TODO Check affixes for pred(a,i,o,u,e)
# https://github.com/rotati/wiki/wiki/Git:-Combine-all-messy-commits-into-one-commit-before-merging-to-Master-branch

TESTS = [5, 6, ]

if __name__ == "__main__":

    from config.postgres import CLIConfig, create_app_lod

    with create_app_lod(CLIConfig).app_context():

        for SELECTOR in TESTS:
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
