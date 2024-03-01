# Script Name: Geo_Data_PreCheck_Script.py
# Description: Checking different conditions on the data related to house numbers and street names
# Date:        16-04-2023


import re
import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('data.xlsx')

# variable used to store the error message in the data
error_name = ""


# function used to check the conditions for Even-House-Numbers
def check_house_even_number(current_index, column_name, row):
    error_name = ""
    if isinstance(row[column_name], float):
        if int(row[column_name]) % 2 != 0 or int(row[column_name]) > 9998:
            error_name += " Index-" + current_index + "_Error-Not-Even-" + column_name + ","

    else:
        if row[column_name] % 2 != 0 or row[column_name] > 9998:
            error_name += " Index-" + current_index + "_Error-Not-Even-" + column_name + ","

    return error_name


# function used to check the conditions for Odd-House-Numbers
def check_house_odd_number(current_index, column_name, row):
    error_name = ""
    if isinstance(row[column_name], float):
        if int(row[column_name]) % 2 == 0 or int(row[column_name]) > 9999:
            error_name += " Ungerade Hausnummer zu groß oder Kommazahl in Zeile " + current_index + ","

    else:
        if row[column_name] % 2 == 0 or row[column_name] > 9999:
            error_name += " Ungerade Hausnummer zu groß oder Kommazahl in Zeile " + current_index + ","

    return error_name


# function used to check the conditions for repeating sub-characters in house-number
def check_repeating_letters(current_index, word_check):
    error_name = ""
    if len(word_check) > 3:
        error_name += "Zeile " + str(current_index) + ": Zu viele Zeichen in HNRZ(Unterzeichen),"

    return error_name


# Loop over each row in the DataFrame
for index, row in df.iterrows():
    # storing the current index of data/row
    current_index = str(index + 2)

    # Check each condition one by one

    # condition to check that street names should be less than 53
    if len(row['STR_BEZ']) >= 52:
        error_name += "Zeile " + str(current_index) + ": Zu viele Zeichen in Adressspalte,"
    elif re.search('\d', row['STR_BEZ']):
        error_name += "Zeile " + str(current_index) + ": Zahlen in Adressspalte,"

    house_numebr_columns = ['HNR_VON_G', 'HNR_BIS_G', 'HNR_VON_U', 'HNR_BIS_U']

    # condition for Even-House-Numbers and 'Von' value should be less than 'BIS' value
    if pd.notna(row['HNR_VON_G']) and pd.isna(row['HNR_BIS_G']):
        error_name += "Zeile " + current_index + ": Fehlende Hausnummer in Spalte HNR_BIS_G, " + check_house_even_number(
            current_index, house_numebr_columns[0], row) + ","

    elif pd.isna(row['HNR_VON_G']) and pd.notna(row['HNR_BIS_G']):
        error_name += "Zeile " + current_index + ": Fehlende Hausnummer in Spalte HNR_VON_G, " + check_house_even_number(
            current_index, house_numebr_columns[1], row) + ","

    elif pd.notna(row['HNR_VON_G']) and pd.notna(row['HNR_BIS_G']):
        if type(row['HNR_BIS_G']) != str and type(row['HNR_VON_G']) != str:
            error_name += check_house_even_number(current_index, house_numebr_columns[0], row)
            error_name += check_house_even_number(current_index, house_numebr_columns[1], row)
            if row['HNR_VON_G'] > row['HNR_BIS_G']:
                error_name += "Zeile " + current_index + ": HNR_BIS_G < HNR_VON_G,"
        else:
            if type(row['HNR_VON_G']) == str and type(row['HNR_BIS_G']) != str:
                error_name += "Zeile " + current_index + ": Zahlen haben Charakter, " + check_house_even_number(
                    current_index, house_numebr_columns[1], row)
            if type(row['HNR_BIS_G']) == str and type(row['HNR_VON_G']) != str:
                error_name += "Zeile " + current_index + ": Zahlen haben Charakter, " + check_house_even_number(
                    current_index, house_numebr_columns[0], row)

    # condition for Odd-House-Numbers and 'Von' value should be less than 'BIS' value
    if pd.notna(row['HNR_VON_U']) and pd.isna(row['HNR_BIS_U']):
        error_name += "Zeile " + current_index + ": Fehlende Hausnummer in Spalte HNR_BIS_U ," + check_house_odd_number(
            current_index,
            house_numebr_columns[
                2], row) + ","

    elif pd.isna(row['HNR_VON_U']) and pd.notna(row['HNR_BIS_U']):
        error_name += "Zeile " + current_index + ": Fehlende Hausnummer in Spalte HNR_VON_U, " + check_house_odd_number(
            current_index,
            house_numebr_columns[
                3], row) + ","

    elif pd.notna(row['HNR_VON_U']) and pd.notna(row['HNR_BIS_U']):
        if type(row['HNR_BIS_U']) != str and type(row['HNR_VON_U']) != str:
            if row['HNR_VON_U'] > row['HNR_BIS_U']:
                error_name += "Zeile " + current_index + ": HNR_BIS_U < HNR_VON_U,"
            error_name += check_house_odd_number(current_index, house_numebr_columns[2], row)
            error_name += check_house_odd_number(current_index, house_numebr_columns[3], row)
        else:
            if type(row['HNR_VON_U']) == str and type(row['HNR_BIS_U']) != str:
                error_name += "Zeile " + current_index + ": Zahlen haben Charakter, " + check_house_odd_number(
                    current_index, house_numebr_columns[3], row)
            if type(row['HNR_BIS_U']) == str and type(row['HNR_VON_U']) != str:
                error_name += "Zeile " + current_index + ": Zahlen haben Charakter, " + check_house_odd_number(
                    current_index, house_numebr_columns[2], row)

    # condition to check repeating letter in House-Number sub characters
    columns = ['HNRZ_VON_G', 'HNRZ_BIS_G', 'HNRZ_VON_U', 'HNRZ_BIS_U']
    for column in columns:
        if pd.notna(row[column]):
            error_name += check_repeating_letters(current_index, row[column])

# printing the final error message
for en in error_name.split(','):
    print(en.strip())
