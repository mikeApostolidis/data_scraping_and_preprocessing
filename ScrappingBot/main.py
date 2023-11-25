import os
import re

import pandas as pd
from unidecode import unidecode

input_folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"

def test_remove_empty_spaces_before_after_commas():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Apply the strip method to each element in the DataFrame
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_convert_excel_to_csv():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Loop through files in the input folder
    for filename in os.listdir(folder):
        if filename.endswith(".xlsx"):
            # Construct the full path of the input Excel file
            input_path = os.path.join(folder, filename)

            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(input_path)

            # Construct the full path of the output CSV file
            output_filename = os.path.splitext(filename)[0] + ".csv"
            output_path = os.path.join(folder, output_filename)

            # Save DataFrame to CSV
            df.to_csv(output_path, index=False)
            # Delete the original Excel file
            os.remove(input_path)
            print(f"Converted {filename} to {output_filename}")


# Function to format CSV files in a folder
def test_remove_first_2_rows_csv():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    # Loop through files in the input folder
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Remove the first two columns
            df = df.iloc[:, 2:]

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame to a new CSV file
            df.to_csv(output_path, index=False)

            print(f"Formatted {filename} and saved as formatted_{filename}")

            # Optionally, you can delete the original CSV file
            # # os.remove(input_path)

            # if "Α/Α" in df.columns and "Α/Α ΡΟΗΣ" in df.columns:
            #     # Drop the columns "A/A" and "A/A"
            #     df = df.drop(columns=["Α/Α", "Α/Α ΡΟΗΣ"])
            #     # print(f"Deleted {filename}")
            # else:
            #     print(f"Columns 'A/A' and 'A/A' not found in {filename}")


def test_normalize_type():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            # Create a mapping dictionary for the ΤΥΠΟΣ column
            type_mapping = {
                'ΓΕΝΙΚΗΣ ΠΑΙΔΕΙΑΣ': 'ΓΕΝΙΚΗΣ',
                'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ': 'ΜΟΥΣΙΚΟ',
            }
            # Use the mapping dictionary to replace values in the ΤΥΠΟΣ column
            df['ΤΥΠΟΣ'] = df['ΤΥΠΟΣ'].replace(type_mapping)

            # For all other values, set the value to 'ΕΙΔΙΚΗΣ'
            df['ΤΥΠΟΣ'] = df['ΤΥΠΟΣ'].apply(lambda x: x if x in ['ΓΕΝΙΚΗΣ', 'ΜΟΥΣΙΚΟ'] else 'ΕΙΔΙΚΗΣ')

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_mitronimo():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΜΗΤΡΩΝΥΜΟ', axis=1)
            except KeyError:
                print("The column 'ΜΗΤΡΩΝΥΜΟ' does not exist.")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_eidikotita():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΕΙΔΙΚΟΤΗΤΑ', axis=1)
            except KeyError:
                print("The column 'ΕΙΔΙΚΟΤΗΤΑ' does not exist.")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_pinakas():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΙΝΑΚΑΣ', axis=1)
            except KeyError:
                print("The column 'ΠΙΝΑΚΑΣ' does not exist.")

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_normalize_perioxi_topothetisis():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('΄', '')
            except KeyError:
                print("The column 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' does not have '΄' string value.")

            try:
                # Remove the character "(Π.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Π.Ε.)', '')
            except KeyError:
                print("The column 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' does not have '(Π.Ε.)' string value.")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('(Δ.Ε.)', '')
            except KeyError:
                print("The column 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' does not have '(Δ.Ε.)' string value.")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('Μειωμένου Ωραρίου', '')
            except KeyError:
                print("The column 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' does not have 'Μειωμένου Ωραρίου' string value.")

            try:
                # Remove the character "(Δ.Ε.)" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'] = df['ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ'].str.replace('-', '')
            except KeyError:
                print("The column 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' does not have '-' string value.")


            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)




def test_dieth_ekps():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('΄', '')
            except KeyError:
                print("The column 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' does not have '΄' string value.")

            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('ΔΙΕΥΘΥΝΣΗ', '')
            except KeyError:
                print("The column 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' does not have 'ΔΙΕΥΘΥΝΣΗ' string value.")
            try:
                # Remove the character "΄" from every row in the 'ΠΕΡΙΟΧΗ ΤΟΠΟΘΕΤΗΣΗΣ' column
                df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'] = df['Δ/ΝΣΗ ΕΚΠ/ΣΗΣ'].str.replace('.', '')
            except KeyError:
                print("The column 'Δ/ΝΣΗ ΕΚΠ/ΣΗΣ' does not have '.' string value.")

            test_remove_empty_spaces_before_after_commas()

            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


def test_delete_periferia():
    folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            # Construct the full path of the input CSV file
            input_path = os.path.join(folder, filename)

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(input_path)

            try:
                # Remove the column named 'ΜΗΤΡΩΝΥΜΟ'
                df = df.drop('ΠΕΡΙΦΕΡΕΙΑ', axis=1)
            except KeyError:
                print("The column 'ΠΕΡΙΦΕΡΕΙΑ' does not exist.")


            # Construct the full path of the output CSV file
            output_path = os.path.join(folder, filename)

            # Save the modified DataFrame back to a new CSV file
            df.to_csv(output_path, index=False)

            # Optionally, you can delete the original CSV file
            # os.remove(input_path)


import mysql.connector

# mydb = mysql.connector.connect(
#         host="localhost",
#         user='eanaplirotes',
#         password="eanaplirotes2023"
#     )
# # Creating an instance of 'cursor' class
# # which is used to execute the 'SQL'
# # statements in 'Python'
# print("Connected to database")
# cursor = mydb.cursor()
# cursor.execute("SHOW TABLES")
# for x in cursor:
#     print(x)


# import pymysql
#
# connection = pymysql.connect(host="eanaplirotes.iee.ihu.gr",
#
#                              user="eanaplirotes",
#
#                              passwd="eanaplirotes2023",
#
#                              database="eanaplirotes")
# cursor = connection.cursor()

# cursor.execute("SELECT * FROM Anaplirotes")
# myresult = cursor.fetchall()
# for x in myresult:
#   print(x)
# some other statements  with the help of cursor
# cursor.close()
