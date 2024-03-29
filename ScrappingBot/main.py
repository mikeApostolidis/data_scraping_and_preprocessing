import inspect
import os
import re
import sys
import traceback

import pytest
import pandas as pd
from unidecode import unidecode

from ScrappingBot.src.scraper.scraper_module import *
from ScrappingBot.src.preprocess.preprocess_module import *
import ScrappingBot.src.settings as settings
from ScrappingBot.src.db.database import connect_to_db, get_max_date


def main():
    path = settings.folder_path
    final_path = settings.final_output_path

    connection = connect_to_db()

    connection.close()

    # Example of using get_max_date
    max_date, max_date = get_max_date()
    result, result = get_max_date()
    print("Max Date from Database:", max_date)

    # Print all columns for each row
    # for row in max_date:
    #     print(row)

    # for row in result:
    #     print(row)
    #     print("\n")

    # path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    # output_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"

    test_remove_all_files(path, final_path)
    try:
        # Scrape data
        scrap(max_date)
    except Exception as e:
        print(f"An error occurred during scraping: {e}", inspect.currentframe().f_lineno)
        traceback.print_exc()

    test_convert_excel_to_csv(path)

    test_remove_empty_spaces_before_after_commas(path)

    test_normalize_columns(path)
    test_delete_AA(path)
    test_delete_AA_ROHS(path)
    test_normalize_type(path)
    test_delete_mitronimo(path)
    # test_delete_eidikotita(path)
    test_delete_pinakas(path)
    test_normalize_perioxi_topothetisis(path)
    test_dieth_ekps(path)
    test_check_moria_pinaka(path)
    test_delete_periferia(path)
    test_add_hmeromhnia(path)
    test_add_orario_values(path)
    test_create_sxoliko_etos(path)
    test_create_sxolia(path)
    test_add_mousika_organa_to_sxolia(path)
    test_remove_empty_spaces_before_after_commas(path)
    re_order(path)

    test_normalize_all_columns_names(path)
    remove_rows_with_empty_names(path)

    test_full_outer_join_csv_files(path, final_path)


if __name__ == "__main__":
    main()
