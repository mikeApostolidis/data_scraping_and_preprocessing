import os
import re

import pandas as pd
from unidecode import unidecode
import numpy as np
from functools import reduce
from datetime import datetime



def test_remove_empty_spaces_before_after_commas(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Apply the strip method to each element in the DataFrame
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            except Exception as e:
                print(f"An error occurred during preprocessing on method  test_remove_empty_spaces_before_after_commas : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def check_if_column_exists(df, column_name, default_value):
    if column_name not in df.columns:
        df[column_name] = default_value


def test_convert_excel_to_csv(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Loop through files in the input folder_path
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            # Construct the full path of the input Excel file
            input_path = os.path.join(folder_path, filename)
            print("input path : ", input_path)

            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(input_path)

            # Construct the full path of the output CSV file
            output_filename = os.path.splitext(filename)[0] + ".csv"
            output_path = os.path.join(folder_path, output_filename)

            # Save DataFrame to CSV
            df.to_csv(output_path, index=False)
            # Delete the original Excel file
            os.remove(input_path)
            print(f"Converted {filename} to {output_filename}")


# Function to format CSV files in a folder_path
# def test_remove_first_2_rows_csv(folder_path):
#     # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
#     # Loop through files in the input folder_path
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".csv"):
#             # Construct the full path of the input CSV file
#             input_path = os.path.join(folder_path, filename)
#
#             # Read CSV file into a pandas DataFrame
#             df = pd.read_csv(input_path)
#
#             # Remove the first two columns
#             df = df.iloc[:, 2:]
#
#             # Construct the full path of the output CSV file
#             output_path = os.path.join(r"C:\Users\mike2\OneDrive\Desktop\sxoli", filename)
#
#             # Save the modified DataFrame to a new CSV file
#             df.to_csv(output_path, index=False)
#
#             print(f"Formatted {filename} and saved as formatted_{filename}")

# Optionally, you can delete the original CSV file
# # os.remove(input_path)
#
# if "Α/Α" in df.columns and "Α/Α ΡΟΗΣ" in df.columns:
#     # Drop the columns "A/A" and "A/A"
#     df = df.drop(columns=["Α/Α", "Α/Α ΡΟΗΣ"])
#     # print(f"Deleted {filename}")
# else:
#     print(f"Columns 'A/A' and 'A/A' not found in {filename}")


def test_delete_AA(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('Α/Α', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method  test_delete_AA : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_AA_ROHS(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('Α/Α ΡΟΗΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method  test_delete_AA_ROHS : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_normalize_type(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Check and add 'ΤΥΠΟΣ' column if it doesn't exist
            check_if_column_exists(df, 'ΤΥΠΟΣ', 'ΚΕΝΟ')

            # Create a mapping dictionary for the ΤΥΠΟΣ column
            type_mapping = {
                'ΓΕΝΙΚΗΣ ΠΑΙΔΕΙΑΣ': 'ΓΕΝΙΚΗΣ',
                'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ': 'ΜΟΥΣΙΚΟ',
            }
            try:

                # Use the mapping dictionary to replace values in the ΤΥΠΟΣ column
                df['ΤΥΠΟΣ'] = df['ΤΥΠΟΣ'].replace(type_mapping)

                # For all other values, set the value to 'ΕΙΔΙΚΗΣ'
                df['ΤΥΠΟΣ'] = df['ΤΥΠΟΣ'].apply(lambda x: x if x in ['ΓΕΝΙΚΗΣ', 'ΜΟΥΣΙΚΟ'] else 'ΕΙΔΙΚΗΣ')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_type : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_mitronimo(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΜΗΤΡΩΝΥΜΟ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_mitronimo : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_eidikotita(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΕΙΔΙΚΟΤΗΤΑ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_eidikotita : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_pinakas(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΙΝΑΚΑΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_pinakas : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_check_moria_pinaka(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)
            try:
                # Check and add 'ΜΟΡΙΑ ΠΙΝΑΚΑ' column if it doesn't exist
                check_if_column_exists(df, 'ΜΟΡΙΑ ΠΙΝΑΚΑ', 0.0)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_check_moria_pinaka : {e},{filename}")

            # try:
            #
            #     # Check if the "moria pinaka" column exists
            #     if "ΜΟΡΙΑ ΠΙΝΑΚΑ" not in df.columns:
            #         # If it doesn't exist, create it with zero values
            #         df["ΜΟΡΙΑ ΠΙΝΑΚΑ"] = 0.0
            # except Exception as e:
            #     print(f"An error occurred during preprocessing : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)


def test_normalize_perioxi_topothetisis(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Check and add 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column if it doesn't exist
            check_if_column_exists(df, 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ', 'ΚΕΝΟ')

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('΄', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis : {e},{filename}")

            try:
                # Remove the character "(Π.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Π.Ε.)', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Δ.Ε.)', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Μειωμένου Ωραρίου', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('-', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_dieth_ekps(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Check and add 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column if it doesn't exist
            check_if_column_exists(df, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ', 'ΚΕΝΟ')

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('΄', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('ΔΙΕΥΘΥΝΣΗ', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")
            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('.', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            test_remove_empty_spaces_before_after_commas(folder_path)

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_periferia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΕΡΙΦΕΡΕΙΑ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_periferia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_create_sxolia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Check and add 'ΩΡΑΡΙΟ' column if it doesn't exist
            check_if_column_exists(df, 'ΩΡΑΡΙΟ', 'ΚΕΝΟ')

            try:
                # Create a new column 'ΣΧΟΛΙΑ' with the values of 'ΩΡΑΡΙΟ'
                df['ΣΧΟΛΙΑ'] = df['ΩΡΑΡΙΟ']
                # Drop the original 'ΩΡΑΡΙΟ' column
                df.drop(columns=['ΩΡΑΡΙΟ'], inplace=True)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_create_sxolia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_add_mousika_organa_to_sxolia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Create a new column 'ΣΧΟΛΙΑ' by concatenating values from 'ΣΧΟΛΙΑ' and 'ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ' with a comma
                df['ΣΧΟΛΙΑ'] = df['ΣΧΟΛΙΑ'] + ', ' + df['ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ']  # prosthetei "" stin teleytaia stili
                # Drop the original columns 'ΩΡΑΡΙΟ' and 'ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ'
                df.drop(columns=['ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ'], inplace=True)
                df.drop(columns=['ΩΡΑΡΙΟ'], inplace=True)

            except Exception as e:
                print(f"An error occurred during preprocessing on method test_add_mousika_organa_to_sxolia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_add_hmeromhnia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):

            # Extract the date from the filename
            match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
            date_from_filename = match.group() if match else None

            if date_from_filename:
                # Construct the full path of the input CSV file
                input_path = os.path.join(folder_path, filename)

                # Read CSV file into a pandas DataFrame
                df = pd.read_csv(input_path)

                # Create a new column and assign the corresponding date
                df['ΗΜΕΡΟΜΗΝΙΑ'] = date_from_filename

                # Construct the full path of the output CSV file
                output_path = os.path.join(folder_path, filename)

                # Save the modified DataFrame back to a new CSV file
                df.to_csv(output_path, index=False)


def test_create_sxoliko_etos(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    global date_object
    # date_object = datetime.today()
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):

            # Extract the date from the filename
            match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
            date_from_filename = match.group() if match else None

            # Extract the year from the filename
            match = re.search(r'\d{4}', filename)
            year_from_filename = match.group() if match else None
            try:
                date_object = datetime.strptime(date_from_filename, "%Y-%m-%d").date()
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_create_sxoliko_etos : {e},{filename}")

            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)
            if year_from_filename:

                try:
                    # Check if the date is in the range from September 1st to December 31st
                    if 1 <= date_object.month <= 8:
                        # Create the 'ΣΧΟΛΙΚΟ ΕΤΟΣ' column
                        df['ΕΤΟΣ'] = f"{int(year_from_filename) - 1}-{year_from_filename}"
                        print("Date is in the range January 1st - August 31st")
                    elif date_object.month >= 9:
                        # Create the 'ΣΧΟΛΙΚΟ ΕΤΟΣ' column
                        df['ΕΤΟΣ'] = f"{year_from_filename}-{int(year_from_filename) + 1}"

                        print("Date is in the range September 1st - December 31st")
                    else:
                        print("Date is not in either range")
                except Exception as e:
                    print(f"An error occurred during preprocessing on method test_create_sxoliko_etos : {e},{filename}, or date {date_object}")

                # Construct the full path of the output CSV file
                output_path = os.path.join(folder_path, filename)

                # Save the modified DataFrame back to a new CSV file
                df.to_csv(output_path, index=False)


def test_add_orario_values(folder_path):
   # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and "ΑΠΩ" in filename:
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            if "ΩΡΑΡΙΟ" not in df.columns:
                # Add the 'ΩΡΑΡΙΟ' column with 'ΑΠΩ' as the default value
                df['ΩΡΑΡΙΟ'] = 'ΑΠΩ'

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)


def test_normalize_all_columns(folder_path):
    #folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Mapping dictionary for Greek to English column names
            column_mapping = {
                'ΤΥΠΟΣ': 'Typos',
                'ΕΠΩΝΥΜΟ': 'Eponymo',
                'ΟΝΟΜΑ': 'Onoma',
                'ΠΑΤΡΩΝΥΜΟ': 'Patronymo',
                'ΚΛΑΔΟΣ': 'Klados',
                'ΣΕΙΡΑ ΠΙΝΑΚΑ': 'Seira_Pinaka',
                'ΜΟΡΙΑ ΠΙΝΑΚΑ': 'Moria_Pinaka',
                'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ': 'Perioxh_Topothethshs',
                'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ': 'Dieytynsh_Ekpaideyshs',
                'ΗΜΕΡΟΜΗΝΙΑ': 'Hmeromnia',
                'ΕΤΟΣ': 'Etos',
                'ΣΧΟΛΙΑ': 'Sxolia',
            }

            try:

                # Keep only the columns present in the mapping dictionary
                df = df[list(column_mapping.keys())]

                # Rename the columns to English names
                df.columns = [column_mapping[col] for col in df.columns]
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_all_columns : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)






def test_full_outer_join_csv_files(folder_path, final_output_path):
    global output_path
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Initialize an empty DataFrame to store the result
    result_df = None
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                # Construct the full path of the input CSV file
                input_path = os.path.join(folder_path, filename)

                # Read CSV file into a pandas DataFrame
                current_df = pd.read_csv(input_path)

                # Perform a full outer join with the result DataFrame
                if result_df is None:
                    result_df = current_df
                else:
                    result_df = pd.merge(result_df, current_df, how='outer')
                # Construct the full path of the output CSV file
                output_path = os.path.join(final_output_path, "merged_output.csv")

        # Save the result DataFrame to a new CSV file
        result_df.to_csv(output_path, index=False)

    except Exception as e:
        print(f"An error occurred during preprocessing on method test_full_outer_join_csv_files : {e}")

