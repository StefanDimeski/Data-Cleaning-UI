import pandas as pd
import json

# Function that processes the file, performs the operation the whole UI is designed to facilitate.
# Returns a Pandas DataFrame containing the processed data.
# Args:
# 1. filepath : String - path to the file to be processed
# 2. id_column : String - name of the column containing the client ID
# 3. date_of_birth_column : String - name of the column containing the date of birth of each client
# 4. columns_to_check_for_total : List[String] - names of the columns that should be checked for having the word "Total" somewhere in them
# 5. columns_for_rule_fixing : List[String] - names of the columns to which the rule-fixing algorithm should be applied.
# 6. columns_to_copy_from_last_total : List[String] - names of the columns that should be copied from the last row containing the word "Total" for each client with multiple entries (EXPLAIN MORE)
# 7. priority_vals : List[String] - list of the values for rule-fixing ordered by priority (first in the list has most priority)
def process_file(filepath, id_column, date_of_birth_column, columns_to_check_for_total, columns_for_rule_fixing, columns_to_copy_from_last_total, priority_vals):
    # get the file extension from the path
    file_extension = filepath.split(".")[-1]

    # use the appropriate pandas f-on to read the file based on its extension/format
    if file_extension == 'csv':
        df = pd.read_csv(filepath)
    elif file_extension == 'xlsx':
        df = pd.read_excel(filepath)
    else:
        print("Shouldn't have gotten here")


    df[date_of_birth_column] = pd.to_datetime(df[date_of_birth_column], format="%d/%m/%Y")
    df[date_of_birth_column] = df[date_of_birth_column].dt.strftime("%d/%m/%Y")

    # fill the missing client IDs using the forward filling method i.e. propagate the last
    # non-null ID to the following rows containing null vals.
    df[id_column].ffill(inplace=True)

    # convert all columns which are not ints or floats to string.
    # The aim is to facilitate the processing happening further down this function,
    # which requires certain columns to be of type string. Could also be rewritten so only
    # those columns get converted to strings if more modularity is required or converting them all
    # creates some problems with certain datatypes
    df = df.astype({column : "string" for column, dtype in zip(df.columns, df.dtypes) if (not 'int' in str(dtype)) or (not 'float' in str(dtype))})

    # replace the null values of the columns that are checked for total with the
    # empty string (""). This is just to make part of the following code simpler,
    # as it only needs to deal with string and not with null values too.
    df[columns_to_check_for_total] = df[columns_to_check_for_total].fillna('')
    
    # get the frequencies of each client ID. The aim is to find the clients which have multiple rows
    # as these are the clients we need to process and "summarise" their rows in a single row.
    counts = df.groupby(id_column).size() 

    # we are only concerned about the duplicates i.e. users that have multiple entries
    duplicates = counts[counts > 1]

    # process each client with multiple rows one by one
    for curr_client_id in duplicates.index.to_list():
        # get the part of the dataframe that refers to the current client
        curr_client_df = df[df[id_column] == curr_client_id]

        # empty dataframe that will store all the rows of the current client
        # which have at least one column(of the columns that are checked for "Total") which contains the word "Total"
        totals_rows = pd.DataFrame()

        # this loop finds all the rows of the current client which contain "Total" and stores them in totals_rows.
        # Does this by iterating through each of the columns that should be checked for "Total"
        # and finding the rows which contain "Total" in that column.
        for column in columns_to_check_for_total:
            # get the rows which contain "Total" in the current column
            curr_totals_rows = curr_client_df[curr_client_df[column].str.contains("Total")]

            # This following if-elif-else code is to fix: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
            # In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
            # To retain the old behavior, exclude the relevant entries before the concat operation.
            if curr_totals_rows.empty:
                continue
            elif totals_rows.empty:
                totals_rows = curr_totals_rows
            else:
                totals_rows = pd.concat([totals_rows, curr_totals_rows])
            # We are sure totals_rows will be sorted properly i.e. as in the original dataframe
            # because of the index of each row which is the row number in the original dataframe.

        # Get all the rows for the current client that are not rows that contain "Total" in at least
        # one column. We do this by excluding, from all the rows of the current client, the rows we found
        # previously to be rows that contain "Total". These are the rows we apply the rule fixing to.
        non_total_rows = curr_client_df.loc[list(set(curr_client_df.index) - set(totals_rows.index))]

        # This loop applies the rules fixing on each column that it is supposed
        # to be applied to, one by one. We accomplish this by getting all the values
        # for the current column and searching for the possible values (given in
        # priority_vals) in order of their priority.
        for column in columns_for_rule_fixing:
            # get the values of all the rows for the current column for the current client in a list
            values = non_total_rows[column].to_list()

            final_val = None

            # Search all the values for the values given in priority_vals. If we find one of them
            # in any row, we have found that value and we store that fact and stop further searching.
            # Because the values given in priority_vals are ordered by their priority, this results in
            # finding the value present which has most priority according to priority_vals.
            for comp in priority_vals:
                containing_values = list(filter(lambda val: comp in val, values))
                if len(containing_values) > 0:
                    final_val = containing_values[0]
                    break

            # if we have found any of the values in priority_vals, then we replace the
            # value in the corresponding column in the first row of the current client with that value
            if final_val is not None:
                df.loc[curr_client_df.index[0], column] = final_val
            # otherwise we replace it with 'Unknown'
            else:
                df.loc[curr_client_df.index[0], column] = 'Unknown'

        # We find the index of the last row which contains "Total" in at least
        # one if its columns. We do this because we want to replace the values of some of the columns
        # of the first row (columns_to_copy_from_last_total) of the current client with the values of those columns in this last row which
        # contains "Total".
                
        # Check if totals_rows is null
        index_of_last_totals_row = max(list(totals_rows.index))

        # Replace the values of the columns listed in columns_to_copy_from_last_total of the first row
        # for the current client with the values of those columns from the last row containing "Total".
        df.loc[curr_client_df.index[0], columns_to_copy_from_last_total] = df.loc[index_of_last_totals_row, columns_to_copy_from_last_total]

        # Remove all the other rows for the current client except for the first row.
        df.drop(curr_client_df.index[1:], inplace=True)

    return df

# Reads the defaults from the defaults.json file that should be
# present in the same folder. If that file is not present, then
# return no defaults.
def read_defaults():
    deserialised = None
    
    # If we can find the file, read it and return the read defaults
    try:
        with open("defaults.json", "r") as f:
            deserialised = json.load(f)
    except:
        # otherwise return no defaults
        return [None, None, [], [], [], []]

    return list(deserialised.values())