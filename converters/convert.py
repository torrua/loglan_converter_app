from converters.ac_to_txt.ac_to_txt_execute import convert_ac_to_txt
from converters.ac_to_pg.ac_to_pg_execute import convert_ac_to_pg

from converters.pg_to_txt.pg_to_txt_execute import convert_pg_to_txt
from converters.pg_to_ac.pg_to_ac_execute import convert_pg_to_ac

from converters.txt_to_pg.txt_to_pg_execute import convert_txt_to_pg
from converters.txt_to_ac.txt_to_ac_execute import convert_txt_to_ac

# TODO sync field types with mdb
# TODO Activate source selection
# TODO Unify logging and resulting

SELECTOR = 4

if __name__ == "__main__":

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
