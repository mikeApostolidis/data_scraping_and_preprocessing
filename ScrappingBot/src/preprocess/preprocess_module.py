import os
import re
import warnings

import numpy as np
import pandas as pd
from datetime import datetime


def test_remove_all_files(path, final_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(path):
        if filename.endswith(".csv") or filename.endswith(".xlsx"):
            # Construct the full path of the file
            file_path = os.path.join(path, filename)
            try:
                # Remove the file
                os.remove(file_path)
            except Exception as e:
                print(
                    f"An error occurred during deleting all csv files on method  test_remove_all_files : {e},{filename}")
    for filename in os.listdir(final_path):
        if filename.endswith(".csv") or filename.endswith(".xlsx"):
            # Construct the full path of the file
            file_path = os.path.join(final_path, filename)
            try:
                # Remove the file
                os.remove(file_path)
            except Exception as e:
                print(
                    f"An error occurred during deleting all csv files on method  test_remove_all_files : {e},{filename}")


def test_remove_empty_spaces_before_after_commas(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Apply the strip method to each element in the DataFrame
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method  test_remove_empty_spaces_before_after_commas : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def check_if_column_exists(df, column_name, default_value):
    if column_name not in df.columns:
        df[column_name] = default_value

def check_if_value_from_row_exists(df, column_name, row_index, default_value=None):
    if column_name not in df.columns:
        df[column_name] = np.nan  # or df[column_name] = default_value if you prefer a specific default
    if pd.isnull(df.at[row_index, column_name]):
        df.at[row_index, column_name] = default_value


def test_convert_excel_to_csv(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Loop through files in the input folder_path
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            # Construct the full path of the input Excel file
            input_path = os.path.join(folder_path, filename)
            # print("input path : ", input_path)

            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(input_path)

            # Construct the full path of the output CSV file
            output_filename = os.path.splitext(filename)[0] + ".csv"
            output_path = os.path.join(folder_path, output_filename)

            # Save DataFrame to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            # Delete the original Excel file
            os.remove(input_path)
            # print(f"Converted {filename} to {output_filename}")


def test_delete_AA(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('Α/Α', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method  test_delete_AA : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_AA_ROHS(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('Α/Α ΡΟΗΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method  test_delete_AA_ROHS : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_normalize_type(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            # Check and add 'ΤΥΠΟΣ' column if it doesn't exist
            check_if_column_exists(df, 'ΤΥΠΟΣ', '')

            try:
                df['ΤΥΠΟΣ'] = df['ΤΥΠΟΣ ΤΟΠΟΘΕΤΗΣΗΣ']
                df = df.drop(['ΤΥΠΟΣ ΤΟΠΟΘΕΤΗΣΗΣ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

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
            # Add an else block to check if the column is empty and fill it with ''
            else:
                if df['ΤΥΠΟΣ'].empty:
                    df['ΤΥΠΟΣ'] = ''

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_mitronimo(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΜΗΤΡΩΝΥΜΟ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_mitronimo : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


# def test_delete_eidikotita(folder_path):
#     # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".csv"):
#             # Construct the full path of the input CSV file
#             input_path = os.path.join(folder_path, filename)
#
#             # Read CSV file into a pandas DataFrame
#             df = pd.read_csv(input_path, encoding='utf-8')
#
#             try:
#                 # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
#                 df = df.drop('ΕΙΔΙΚΟΤΗΤΑ', axis=1)
#             except Exception as e:
#                 print(f"An error occurred during preprocessing on method test_delete_eidikotita : {e},{filename}")
#
#             # Construct the full path of the output CSV file
#             output_path = os.path.join(folder_path, filename)
#
#             # Save the modified DataFrame back to a new CSV file
#             df.to_csv(output_path, index=False, encoding='utf-8')
#
#             # Optionally, you can delete the original CSV file
#             # os.remove(input_path)


def test_delete_pinakas(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΙΝΑΚΑΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_pinakas : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_check_moria_pinaka(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')
            try:
                # Check and add 'ΜΟΡΙΑ ΠΙΝΑΚΑ' column if it doesn't exist
                check_if_column_exists(df, 'ΜΟΡΙΑ ΠΙΝΑΚΑ', None)
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
            df.to_csv(output_path, index=False, encoding='utf-8')


def test_normalize_perioxi_topothetisis(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            # Check and add 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column if it doesn't exist
            check_if_column_exists(df, 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ', '')
            try:

                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Α.Μ.Ω.', '')
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Α.Π.Ω.', '')
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('ΑΠΩ', '')
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('ΑΜΩ', '')

            except Exception as e:
                print(f"An error occurred during preprocessing: {e}, {filename}")
            try:
                # Remove "B-" prefix from the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Β-', '')
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis(1) : {e},{filename}")
            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('΄', '')
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis(1) : {e},{filename}")

            try:
                # Remove the character "(Π.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Π.Ε.)', '')
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis(2) : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Δ.Ε.)', '')
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis(3) : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Μειωμένου Ωραρίου', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method : {e},{filename}")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('-', '')
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('  ', ' ')
            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_normalize_perioxi_topothetisis(4) : {e},{filename}")
                # Remove key words from the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_dieth_ekps(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Dictionary of key phrases and their corresponding values
    key_phrases_PE_DE = {
        'Π.Ε.',
        'Δ.Ε.'
    }

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            # Check and add 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column if it doesn't exist
            check_if_column_exists(df, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ', '')

            try:
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ Α/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ']
                df = df.drop(['Δ/ΝΣΗ Α/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")
            try:
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ Π/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ']
                df = df.drop(['Δ/ΝΣΗ Π/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")
            try:
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΠΡΩΤΟΒΑΘΜΙΑΣ ΕΚΠ/ΣΗΣ']
                df = df.drop(['Δ/ΝΣΗ ΠΡΩΤΟΒΑΘΜΙΑΣ ΕΚΠ/ΣΗΣ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            # Check if values in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column are equal to '-'
            condition = (df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] == '-')

            # Replace '-' with None only where the condition is True
            df.loc[condition, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = None

            try:
                # Remove the character "ΔΙΕΥΘΥΝΣΗ" from every row in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('ΔΙΕΥΘΥΝΣΗ', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                df['Suffix'] = ''  # Initialize 'Suffix' before the loop
                for index, row in df.iterrows():
                    suffix_position = str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ']).find('΄')
                    if suffix_position != -1 and suffix_position > 0:
                        # Store the character before '΄' in the 'Suffix' column
                        df.at[index, 'Suffix'] = str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'])[suffix_position - 1]
                        # Remove only the character before '΄'
                        df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = (
                                str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'])[:suffix_position - 1] +
                                str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'])[suffix_position:]
                        ).strip()
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                # Remove the character "΄" from every row in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('΄', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")
            try:
                df['Prefix'] = ''
                for index, row in df.iterrows():
                    for key_phrase in key_phrases_PE_DE:
                        if key_phrase in str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ']):
                            # df['Prefix'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.split(' ', n=1).str[0]
                            # df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.split(' ', n=1).str[1]
                            # Store the matched phrase in the 'Prefix' column
                            matched_phrase = key_phrase

                            # Update the 'Prefix' column
                            df.at[index, 'Prefix'] = matched_phrase

                            # Remove the matched phrase from the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                            df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = str(df.at[index, 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ']).replace(matched_phrase,
                                                                                                       '').strip()

                # print(df['Prefix'])
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                # reconstruct the column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Prefix'] + ' ' + df['Suffix'] + ' ' + df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ']
            # df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Suffix'] + '$ ' + df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ']
            except Exception as e:
                print(f"An error occurred during changing suffix: {e}")

            try:
                # Remove the character "." from every row in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('.', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                # Remove the character "." from every row in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('  ', ' ')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            try:
                # Remove the character "." from every row in the 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('()', '')
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_dieth_ekps : {e},{filename}")

            df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].fillna('')

            # Drop the 'Suffix' and 'Prefix' columns
            df = df.drop(['Suffix', 'Prefix'], axis=1)

            output_path = os.path.join(folder_path, filename)

            df.to_csv(output_path, index=False, encoding='utf-8')


def test_delete_periferia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΕΡΙΦΕΡΕΙΑ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_delete_periferia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_create_sxolia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

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
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_add_mousika_organa_to_sxolia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Create a new column 'ΣΧΟΛΙΑ' by concatenating values from 'ΣΧΟΛΙΑ' and 'ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ' with a comma
                df['ΣΧΟΛΙΑ'] = df['ΣΧΟΛΙΑ'] + ', ' + df['ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ']  # prosthetei "" stin teleytaia stili
                # Drop the original columns 'ΩΡΑΡΙΟ' and 'ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ'
                df.drop(columns=['ΜΟΥΣΙΚΗ ΕΙΔΙΚΕΥΣΗ'], inplace=True)
                df.drop(columns=['ΩΡΑΡΙΟ'], inplace=True)

            except Exception as e:
                print(
                    f"An error occurred during preprocessing on method test_add_mousika_organa_to_sxolia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_add_hmeromhnia(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            try:
                # Extract the date from the filename
                match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
                date_from_filename = match.group() if match else None

                if date_from_filename:
                    # Construct the full path of the input CSV file
                    input_path = os.path.join(folder_path, filename)

                    # Read CSV file into a pandas DataFrame
                    df = pd.read_csv(input_path, encoding='utf-8')

                    # Create a new column and assign the corresponding date
                    df['ΗΜΕΡΟΜΗΝΙΑ'] = date_from_filename
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_add_hmeromhnia : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')


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
            df = pd.read_csv(input_path, encoding='utf-8')
            if year_from_filename:

                try:
                    # Check if the date is in the range from September 1st to December 31st
                    if 1 <= date_object.month <= 8:
                        # Create the 'ΣΧΟΛΙΚΟ ΕΤΟΣ' column
                        df['ΕΤΟΣ'] = f"{int(year_from_filename) - 1}-{year_from_filename}"
                        # print("Date is in the range January 1st - August 31st")
                    elif date_object.month >= 9:
                        # Create the 'ΣΧΟΛΙΚΟ ΕΤΟΣ' column
                        df['ΕΤΟΣ'] = f"{year_from_filename}-{int(year_from_filename) + 1}"

                        # print("Date is in the range September 1st - December 31st")
                    else:
                        print("Date is not in either range")
                except Exception as e:
                    print(
                        f"An error occurred during preprocessing on method test_create_sxoliko_etos : {e},{filename}, or date {date_object}")

                # Construct the full path of the output CSV file
                output_path = os.path.join(folder_path, filename)

                # Save the modified DataFrame back to a new CSV file
                df.to_csv(output_path, index=False, encoding='utf-8')


def test_add_orario_values(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and "ΑΠΩ" in filename:
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')

            if "ΩΡΑΡΙΟ" not in df.columns:
                # Add the 'ΩΡΑΡΙΟ' column with 'ΑΠΩ' as the default value
                df['ΩΡΑΡΙΟ'] = 'ΑΠΩ'

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')


def test_normalize_columns(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)

            df = pd.read_csv(input_path, encoding='utf-8')

            try:
                # Check if the 'ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ' column exists in the DataFrame
                if 'ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ' in df.columns:
                    # Keep only the 'ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ' column
                    df['ΚΛΑΔΟΣ'] = df['ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ']
                elif 'ΚΛΑΔΟΣ / ΕΙΔΙΚΟΤΗΤΑ' in df.columns:
                    # Keep only the 'ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ' column
                    df['ΚΛΑΔΟΣ'] = df['ΚΛΑΔΟΣ / ΕΙΔΙΚΟΤΗΤΑ']

                    # Drop the original 'ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ' column
                    df = df.drop(['ΚΛΑΔΟΣ/ ΕΙΔΙΚΟΤΗΤΑ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")
            try:
                df['ΚΛΑΔΟΣ'] = df['ΕΙΔΙΚΟΤΗΤΑ']
                df = df.drop(['ΕΙΔΙΚΟΤΗΤΑ'], axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΣΧΟΛΙΚΗ ΜΟΝΑΔΑ ΤΟΠΟΘΕΤΗΣΗΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΣΧΟΛΙΚΗ ΜΟΝΑΔΑ ΤΟΠΟΘΕΤΗΣΗΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('Τύπος Πρόσληψης', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΤΡΙΤΕΚΝΟΣ', axis=1)
            except Exception as e:
                print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            # try:
            #
            #     df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ Α/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ']
            #     df = df.drop(['Δ/ΝΣΗ Α/ΘΜΙΑΣ ΕΚΠ/ΣΗΣ'], axis=1)
            # except Exception as e:
            #     print(f"An error occurred during preprocessing on method test_normalize_columns : {e},{filename}")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')


def test_normalize_all_columns_names(folder_path):
    # folder_path = r"C:\Users\mike2\OneDrive\Desktop\sxoli\preprocess_folder"

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder_path, filename)
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
            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path, encoding='utf-8')
            try:
                # Keep only the columns present in the mapping dictionary
                df = df[list(column_mapping.keys())]

                # Rename the columns to English names
                df.columns = [column_mapping[col] for col in df.columns]

            except Exception as e:

                print(f"An error occurred during preprocessing on method test_normalize_all_columns : {e},{filename}")
                # Check if all desired columns exist in the DataFrame

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder_path, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False, encoding='utf-8')


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
                current_df = pd.read_csv(input_path, encoding='utf-8')

                # Fill all NaN values in the current DataFrame with ''
                current_df = current_df.fillna('')

                current_df['Moria_Pinaka'] = pd.to_numeric(current_df['Moria_Pinaka'], errors='coerce').fillna(0.0).astype(float)
                current_df['Seira_Pinaka'] = pd.to_numeric(current_df['Seira_Pinaka'], errors='coerce').fillna(0).astype(int)
                # Perform a full outer join with the result DataFrame
                if result_df is None:
                    result_df = current_df
                else:
                    try:
                        # Fill NaN values in the result DataFrame with ''
                        result_df = result_df.fillna(np.nan)

                        # current_df['Seira_Pinaka'] = pd.to_numeric(current_df['Seira_Pinaka'], errors='coerce').fillna(
                        #     0).astype(int)
                        # # current_df['Moria_Pinaka'] = current_df['Moria_Pinaka'].fillna(None)
                        # current_df['Moria_Pinaka'] = pd.to_numeric(current_df['Moria_Pinaka'], errors='coerce').fillna(
                        #     0.0).astype(float)
                        result_df = pd.merge(result_df, current_df, how='outer')
                    except Exception as e:
                        print(f"An error occurred during preprocessing on method test_full_outer_join_csv_files : {e}")
                    except pd.errors.MergeError as merge_error:
                        # Print a warning message and continue with the next file
                        warnings.warn(f"Warning in file {filename}: {merge_error}")
                # Construct the full path of the output CSV file
                output_path = os.path.join(final_output_path, "merged_output.csv")

        # Save the result DataFrame to a new CSV file
        result_df.to_csv(output_path, index=False, encoding='utf-8')

    except Exception as e:
        print(f"An error occurred during preprocessing on method test_full_outer_join_csv_files : {e}")


def re_order(folder_path):
    desired_order = ['ΤΥΠΟΣ', 'ΕΠΩΝΥΜΟ', 'ΟΝΟΜΑ', 'ΠΑΤΡΩΝΥΜΟ', 'ΚΛΑΔΟΣ', 'ΣΕΙΡΑ ΠΙΝΑΚΑ', 'ΜΟΡΙΑ ΠΙΝΑΚΑ',
                     'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ', 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ', 'ΗΜΕΡΟΜΗΝΙΑ', 'ΕΤΟΣ', 'ΣΧΟΛΙΑ']
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                # Construct the full path of the input CSV file
                input_path = os.path.join(folder_path, filename)

                # Read CSV file into a pandas DataFrame
                df = pd.read_csv(input_path, encoding='utf-8')

                # Handle missing columns
                missing_columns = set(desired_order) - set(df.columns)
                for missing_column in missing_columns:
                    df[missing_column] = None  # You can modify this to assign a default value

                # Remove extra columns
                extra_columns = set(df.columns) - set(desired_order)
                df = df.drop(columns=extra_columns, errors='ignore')

                # Reorder columns based on the desired order
                df = df[desired_order]

                # Reorder columns based on the desired order
                df = df[desired_order]

                # Construct the full path of the output CSV file
                output_path = os.path.join(folder_path, filename)

                # Save the modified DataFrame back to a new CSV file
                df.to_csv(output_path, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred during preprocessing on method test_full_outer_join_csv_files : {e}")


def remove_rows_with_empty_names(folder_path):
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                # Construct the full path of the input CSV file
                input_path = os.path.join(folder_path, filename)

                # Read CSV file into a pandas DataFrame
                df = pd.read_csv(input_path, encoding='utf-8')

                # Check if 'ΕΠΩΝΥΜΟ', 'ΟΝΟΜΑ', and 'ΠΑΤΡΩΝΥΜΟ' columns are empty
                condition = df['Eponymo'].isnull() & df['Onoma'].isnull() & df['Patronymo'].isnull()

                # Remove rows that meet the condition
                df = df[~condition]

                # Save the modified DataFrame back to the original CSV file (overwrite)
                df.to_csv(input_path, index=False, encoding='utf-8')

    except Exception as e:
        print(f"An error occurred during preprocessing on method remove_rows_with_empty_names : {e}")
